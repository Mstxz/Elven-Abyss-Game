from godot import exposed, export
from godot import *
import random

@exposed
class ExplodingEnemy(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=100.0)
	atk = export(float, default=50.00)
	maxhp = export(float, default=100.0)
	hp = export(float, default=100.0)
	defense = export(float, default=0.0)
	exp = export(float, default=10.0)
	gold = export(float, default=10.0)
	acting = export(bool, default=False)
	randomwalking = export(bool, default=True)
	freeze = export(bool, default=False)
	died = export(bool, default=False)
	randomwalkdelaysent = False
	randomdirection = Vector2(random.randrange(-100,100),random.randrange(-100,100)) #random direction
	player = None #use to store player object
	knockbacked = Vector2() #set in take_damage and reduce by a rate in each _progress
	velocity = Vector2()
	
	def _ready(self):
		'''runs when object spawn'''
		#prepares require nodes
		self.sprite = self.get_node("AnimatedSprite") #enemy sprite
		self.healthbar = self.get_node("Viewport/HealthBar") #enemy healthbar
		self.hitbox = self.get_node("Hitbox")
		self.animplayer = self.get_node("AnimationPlayer")
	
	def _process(self, delta):
		'''runs every frame'''
		if self.died or self.freeze:
			return
		self.movement() #check movement every frames
		if not self.acting and self.player:
			distance = self.player.position.distance_to(self.position)
			miny = range(int(self.position.y-20),int(self.position.y+20))
			if distance < 30:
				#attack if in range
				self.attack()
		
	
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
	
	def movement(self):
		'''handle all kind of enemy movement'''
		direction = Vector2(0,0)
		if abs(self.knockbacked.x) + abs(self.knockbacked.y) > 5:
			# in case theres no player in range and theres still kb
			# so this have to be outside main if
			self.velocity *= 0.9
			self.knockbacked *= 0.9
			# Move the enemy using move_and_slide for proper physics handling
			self.move_and_slide(self.velocity)
		
		elif self.player and not self.acting: #if there is player in sight:
			#get direction
			direction = self.player.position - self.position
			
			self.flip(direction)
			
			#normalize direction
			direction = direction.normalized()
			self.velocity = direction * self.speed
			self.knockbacked *= 0
		elif not self.acting and not self.player:
			direction = self.randomwalk()
			self.velocity = direction * self.speed
			
		if not self.acting:
			
			if abs(direction.x) + abs(direction.y > 0):
				self.sprite.play('Walk')
			else:
				self.sprite.play('Idle')
				
			self.move_and_slide(self.velocity)
	
	def randomwalk(self,command=None):
		'''Enable random walking whie player not in sight'''
		#random movement
		if command: #convert gdstring to string
			command = str(command)
		direction = Vector2(0,0)
		if self.randomwalking and not self.acting and not command:
			#Walking
			direction = self.randomdirection
			self.flip(direction)
			self.velocity = direction * self.speed
			if not self.randomwalkdelaysent:
				#Stop after 2 sec
				self.randomwalkdelaysent = True
				self.wait(random.uniform(1.0,2.0),'randomwalk',['stop'])
		elif command == 'stop':
			self.randomwalkdelaysent = False
			self.randomwalking = False
			self.randomdirection = Vector2(random.randrange(-100,100),random.randrange(-100,100))
			direction = Vector2(0,0)
			self.velocity = direction * self.speed
			self.wait(random.uniform(1.0,3.0),'randomwalk',['reset']) #delay for make it stay for second
		elif command == 'reset':
			self.randomwalking = True #change state to start new random
		direction = direction.normalized()
		
		return direction
	
	def flip(self, direction):
		"""flip sprite"""
		if direction.x < 0: #flip sprite depending on what direction its running to
			self.sprite.flip_h = False
		else:
			self.sprite.flip_h = True

	def _on_Area2D_body_entered(self, body):
		'''when player in area2d, enemy will see'''
		if str(body.name) == "Player": #prevent recognizing other kinematic2d
			self.player = body
		
	def _on_Area2D_body_exited(self, body):
		'''unsee player'''
		if str(body.name) == "Player": #prevent recognizing other kinematic2d
			self.player = None

	def attack(self,part=0):
		'''attack function'''
		if not part:
			self.died = True
			self.sprite.play("Attack")
			self.acting = True
			self.sprite.connect("animation_finished",self,"attack",Array([part+1]))
			self.animplayer.play('ExplodeLight')
			self.animplayer.connect("animation_finished",self,"death")
		elif part == 1:
			allbodies = self.get_node("Hitbox").get_overlapping_bodies()
			self.sprite.queue_free()
			self.get_node("VirtualHealthBar").queue_free()
			for i in allbodies:
				if str(i.name) == "Player": #prevent recognizing other kinematic2d
					direction = self.player.position - self.position
					knockback = Vector2(300,0).rotated(direction.angle())
					dmg = self.atk
					self.hitbox.scale = Vector2(0,0)
					self.player.take_damage(self.atk,knockback)
		
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
		if kb: #kb stands for knockback
			self.velocity = kb
			self.knockbacked = kb
			self.move_and_slide(self.velocity)
		if dmg: #handle dmg
			self.hp -= dmg
			self.hp_changed_func()
		if self.hp <= 0: #if health <= 0 then call death func
			self.death()
		
	def heal(self, amount): 
		'''handle heals'''
		self.hp += amount
