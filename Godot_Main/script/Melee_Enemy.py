from godot import exposed, export
from godot import *
import random

@exposed
class Melee_Enemy(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=60.0)
	atk = export(float, default=10.00)
	maxhp = export(float, default=100.0)
	hp = export(float, default=100.0)
	defense = export(float, default=0.0)
	acting = export(bool, default=False)
	randomwalk = export(bool, default=False)
	player = None #use to store player object
	knockbacked = Vector2() #set in take_damage and reduce by a rate in each _progress
	velocity = Vector2()
	def _ready(self):
		'''runs when object spawn'''
		#prepares require nodes
		self.sprite = self.get_node("AnimatedSprite") #enemy sprite
		self.healthbar = self.get_node("Viewport/HealthBar") #enemy healthbar
		self.hitbox = self.get_node("Hitbox")
	
	def _process(self, delta):
		'''runs every frame'''
		self.movement() #check movement every frames
		if not self.acting and self.player:
			self.randomwalk = False
			distance = self.player.position.distance_to(self.position)
			miny = range(int(self.position.y-20),int(self.position.y+20))
			if distance < 30 and int(self.player.position.y) in miny:
				#attack if in range
				self.attack()
		if not self.acting:
			self.sprite.play('Idle')
	
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
	
	def movement(self, part=0):
		'''handle all kind of enemy movement'''
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
			
			#in case you start to get close
			distance = self.player.position.distance_to(self.position)
			if distance < 50:
				#change position to left or right of player
				direction = Vector2(direction.x*0.5,self.player.position.y - self.position.y)
				if distance < 30: #made to make the slime walk beside player when too close
					simposleft = Vector2(self.player.position.x-35,self.player.position.y)
					simposright = Vector2(self.player.position.x+35,self.player.position.y)
					leftdis = simposleft.distance_to(self.position)
					rightdis = simposright.distance_to(self.position)
					simposmin = min(leftdis,rightdis)
					if simposmin == leftdis:
						direction = simposleft - self.position
					else:
						direction = simposright - self.position
			
			#normalize direction
			direction = direction.normalized()
			self.velocity = direction * self.speed
			self.knockbacked *= 0
			self.move_and_slide(self.velocity)

		elif not self.player:
			#random movement
			if not self.randomwalk:
				self.randomwalk = True
				direction = Vector2(0,0)
				state1 = random.randrange(0,3) #random direction x
				state2 = random.randrange(0,3) #random direction y

				if state1 == 1:
					direction.x = 100
				elif state1 == 2:
					direction.x = -100
				if state2 == 1:
					direction.y = 100
				elif state2 == 2:
					direction.y = -100

				self.flip(direction)
				direction = direction.normalized()
				self.velocity = direction * self.speed
				self.wait(1.5,'movement',[part+1]) #delay for move

			if part == 1:
				direction = Vector2(0,0)
				direction = direction.normalized()
				self.velocity = direction * self.speed
				self.wait(1,'movement',[part+1]) #delay for make it stay for second

			elif part == 2:
				self.randomwalk = False #change state to start new random

			self.move_and_slide(self.velocity)

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

	def _on_Hitbox_body_entered(self, body):
		'''player will tkae damage when enter area'''
		if str(body.name) == "Player": #prevent recognizing other kinematic2d
			direction = self.player.position - self.position
			knockback = Vector2(300,0).rotated(direction.angle())
			dmg = self.atk/10
			self.hitbox.scale = Vector2(0,0)
			if self.acting:
				knockback.x *= 0.75
				knockback.y = 0
				dmg = self.atk
			self.player.take_damage(self.atk,knockback)
	
	def _on_Hitbox_body_exited(self, body):
		'''player will tkae damage when enter area'''

	def hitbox_change(self,command):
		'''change hitbox position to deal damage to player'''
		if command == 'reset':
			self.hitbox.position = Vector2(0,0)
			self.hitbox.scale = Vector2(0,0)
		elif command == 'update':
			direction = self.player.position - self.position
			if direction.x < 0:
				self.hitbox.position = Vector2(-20,0) #change hitbox position
			else:
				self.hitbox.position = Vector2(20,0) #change hitbox position
			self.hitbox.scale = Vector2(1,1)
	def attack(self,part=0):
		'''attack function'''
		delay = 0
		if not part and not self.acting:
			self.acting = True
			self.sprite.play("Attack")
			self.wait(0.2,'attack',Array([part+1]))
		elif part == 1:
			self.hitbox_change('update')
			self.wait(0.2,'attack',Array([part+1]))
		elif part == 2:
			self.wait(0.2,'cooldown')
			self.wait(0.2,'attack',Array([part+1]))
		elif part == 3:
			self.hitbox_change('reset')
		
	def hp_changed_func(self):
		'''update the health'''
		self.healthbar.updatehealth(self.maxhp,self.hp) 
	
	def death(self):
		'''deletes itself'''
		self.queue_free()
	
	def take_damage(self, dmg, kb=None):
		'''handle taking damage'''
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
