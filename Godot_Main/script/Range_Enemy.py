from godot import exposed, export
from godot import *
import random, math

projectile = ResourceLoader.load("res://scene/Arrow.tscn")

@exposed
class Range_Enemy(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=100.00)
	rotation_speed = export(float, default=130.00)
	atk = export(float, default=10.00)
	maxhp = export(float, default=100.0)
	hp = export(float, default=100.0)
	defense = export(float, default=0.0)
	player = None #use to store player objects
	acting = export(bool, default=False)
	knockbacked = Vector2() #set in take_damage and reduce by a rate in each _progress
	velocity = Vector2()
	minrange = 130 #minimum distance until enemy runs away from player
	maxrange = 150 #maximum distance until enemy runs into player
	angle = 0
	
	def _ready(self):
		'''runs when object spawn'''
		#prepares require nodes
		self.sprite = self.get_node("AnimatedSprite") #enemy sprite
		self.healthbar = self.get_node("Viewport/HealthBar") #enemy healthbar
		self.main = self.get_node("/root/Node2D")
	
	def _process(self, delta):
		'''runs every frame'''
		self.movement(delta) #check movement every frames
		if not self.acting and self.player and self.player.position.distance_to(self.position) <= self.maxrange:
			self.shoot()
		
	def movement(self, delta, part=0):
		'''handle all kind of enemy movement'''
		if abs(self.knockbacked.x) + abs(self.knockbacked.y) > 5:
			# in case theres no player in sight and theres still kb
			# so this have to be outside main if condition
			self.velocity *= 0.9
			self.knockbacked *= 0.9
			if not self.player:
				# Move the enemy using move_and_slide for proper physics handling
				self.move_and_slide(self.velocity)
		
		if self.player: #when there is player in sight
			distance = self.player.position.distance_to(self.position)
			
			direction = Vector2(0,0)
			#if enemy is in the right distance then don't need to move
			if distance in range(self.minrange,self.maxrange):
				return
			
			#change direction base on whether the player is too close or far
			if distance < self.minrange:
				direction = -(self.player.position - self.position)
			elif distance > self.maxrange:
				direction = (self.player.position - self.position)
			else:
				# Set a fixed radius for the circular motion
				radius = self.maxrange
				# Calculate the angle between the enemy and the player
				angle_to_player = math.atan2(self.position.y - self.player.position.y, self.position.x - self.player.position.x)
				# Update the angle slightly every frame to rotate around the player smoothly
				angle_to_player += self.rotation_speed * delta

				# Calculate the new position on the circular path around the player
				new_x = self.player.position.x + radius * math.cos(angle_to_player)
				new_y = self.player.position.y + radius * math.sin(angle_to_player)

				# Set the new direction to move along the circle (towards the calculated position)
				direction = Vector2(new_x - self.position.x, new_y - self.position.y)

			self.flip(direction)

			# Normalize direction
			direction = direction.normalized()

			# If the knockbacked are not reduced enough do not move
			# or else it would set the velocity thus ends the knockback
			if abs(self.knockbacked.x) + abs(self.knockbacked.y) < 5:
				#walking
				self.velocity = direction * self.speed
				self.knockbacked *= 0
			
			# Move the enemy using move_and_slide for proper physics handling
			self.move_and_slide(self.velocity)

		else:
			#random movement
			if not self.acting:
				self.acting = True
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
				self.acting = False #change state to start new random

			self.move_and_slide(self.velocity)
	
	def flip(self, direction):
		"""flip sprite"""
		if direction.x < 0: #flip sprite depending on what direction its running to
			self.sprite.flip_h = False
		else:
			self.sprite.flip_h = True

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
	
	def cleartimer(self,timer):
		'''sole purpose to delete timer made from wait()'''
		timer.queue_free()
	
	def cooldown(self):
		'''frequently use to let the player act after the timer'''
		self.acting = False
	
	def shoot(self,part=0):
		'''enemy shoots projectile toward player'''
		if not part:
			if not self.acting:
				#acting is as it name suggest to prevent spam and
				#keep the animation running
				self.acting = True
				#self.sprite.play()
				if self.player.position.x > self.position.x:
					self.sprite.flip_h = True
				else:
					self.sprite.flip_h = False
				self.wait(0.3,'shoot',[part+1])
		elif part == 1:
			# 'projectile' is loaded scene sees at the start of this script
			bullet = projectile.instance()
			#get direction from mousepos turn it into proper angle value
			direction = (self.position - self.player.position).angle()
			#set projectile property
			bullet.direction = direction
			bullet.spawnpos = self.position + (self.position - self.player.position) * -0.22
			bullet.spawnrot = direction
			bullet.speed = 50
			bullet.duration = 6
			#add it
			self.main.add_child(bullet)
			
			#set self.acting back to False after the set time
			self.wait(1,'cooldown')
	
	def _on_Area2D_body_entered(self, body):
		'''when player in area2d, enemy will see'''
		if str(body.name) == "Player": #prevent recognizing other kinematic2d
			self.player = body
		
	def _on_Area2D_body_exited(self, body):
		'''unsee player'''
		if str(body.name) == "Player": #prevent recognizing other kinematic2d
			self.player = None
	
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
	
	
