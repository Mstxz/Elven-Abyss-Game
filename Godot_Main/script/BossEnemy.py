from godot import exposed, export
from godot import *
import random

projectile = ResourceLoader.load("res://scene/ShadowBall.tscn")

@exposed
class BossEnemy(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=70.0)
	atk = export(float, default=10.00)
	maxhp = export(float, default=300.0)
	hp = export(float, default=300.0)
	defense = export(float, default=10.0)
	exp = export(float, default=10.0)
	gold = export(float, default=10.0)
	acting = export(bool, default=False)
	died = export(bool, default=False)
	freeze = export(bool, default=False)
	player = None #use to store player object
	velocity = Vector2()
	
	def _ready(self):
		'''runs when object spawn'''
		#prepares require nodes
		self.sprite = self.get_node("AnimatedSprite") #enemy sprite
		#self.healthbar = self.get_node("Viewport/HealthBar") #enemy healthbar
		self.hitbox = self.get_node("Hitbox")
		self.animplayer = self.get_node("AnimationPlayer")
		self.main = self.get_parent()
		self.healthbar = self.main.get_node('BossHealthBar').get_node('HealthBar')
		
	def _process(self, delta):
		'''runs every frame'''
		if self.died:
			return
		if self.freeze:
			self.freeze = False
			self.take_damage(20)
			self.player.removefrombubble(self)
		self.summonshadowball()
		if not self.player:
			self.player = self.main.get_node('Player')
		
	def summonshadowball(self,part=0):
		'''Summon ShadowBall'''
		if not self.acting and not part:
			self.acting = True
			for i in range(15):
				bullet = projectile.instance()
				randomx = random.randrange(-200,200)
				randomy = random.randrange(-300,-270)
				#get direction from mousepos turn it into proper angle value
				direction = (Vector2(randomx,-500) - Vector2(randomx,randomy)).angle()
				#set projectile property
				bullet.direction = direction
				bullet.spawnpos = Vector2(randomx,randomy)
				bullet.spawnrot = direction
				bullet.speed = random.randrange(80,250)
				bullet.duration = 20
				#add it
				self.main.add_child(bullet)
			self.wait(1,'summonshadowball',[part+1])
		elif part == 1:
			for i in range(10):
				bullet = projectile.instance()
				randomx = random.randrange(-200,200)
				randomy = random.randrange(-300,-270)
				#get direction from mousepos turn it into proper angle value
				direction = (Vector2(randomx,-500) - Vector2(randomx,randomy)).angle()
				#set projectile property
				bullet.direction = direction
				bullet.spawnpos = Vector2(randomx,randomy)
				bullet.spawnrot = direction
				bullet.speed = random.randrange(80,250)
				bullet.duration = 20
				#add it
				self.main.add_child(bullet)
			self.wait(10,'cooldown')
	def wait(self,time,funcname,para=Array()):
		'''see example in shoot()'''
		timer = Timer.new()
		timer.one_shot = True
		self.add_child(timer)
		
		# Connect the timeout signal to a custom method
		timer.connect("timeout", self, funcname, Array(para))
		timer.connect("timeout", self, 'cleartimer', Array([timer]))
		# Start the timer
		timer.start(time)
	
	def cooldown(self):
		'''frequently use to let the enemies act after the timer'''
		self.acting = False
		
	def cleartimer(self,timer):
		'''sole purpose to delete timer made from wait()'''
		timer.queue_free()

	def attack(self,part=0):
		'''attack function'''
		
	def hp_changed_func(self):
		'''update the health'''
		self.healthbar.updatehealth(self.maxhp,self.hp) 
	
	def death(self,param=None):
		'''deletes itself'''
		if not self.died: #death animation
			self.died = True
			self.animplayer.play('Die')
			self.animplayer.connect("animation_finished",self,"death")
			return
		self.player = self.get_node("../Player")
		if self.freeze:
			self.player.removefrombubble(self)
		self.player.gain_exp(self.exp)
		self.player.money_modify(self.gold)
		self.queue_free()
	
	def take_damage(self, dmg, kb=None):
		'''handle taking damage'''
		if self.died:
			return
		#reduce damage with defense with the least possible dmg is 1
		dmg = max(dmg-self.defense, 1) 
		if dmg: #handle dmg
			self.hp -= dmg
			self.hp_changed_func()
		if self.hp <= 0: #if health <= 0 then call death func
			self.death()
		
	def heal(self, amount): 
		'''handle heals'''
		self.hp += amount
