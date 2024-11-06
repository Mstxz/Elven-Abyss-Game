from godot import exposed, export
from godot import *


@exposed
class BossEnemy(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=70.0)
	atk = export(float, default=10.00)
	maxhp = export(float, default=100.0)
	hp = export(float, default=100.0)
	defense = export(float, default=0.0)
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
	
	def _process(self, delta):
		'''runs every frame'''
		if self.died or self.freeze:
			return
		
	
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
