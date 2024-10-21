from godot import exposed, export
from godot import *


@exposed
class Range_Enemy(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=100.00)
	atk = export(float, default=10.00)
	maxhp = export(float, default=100.0)
	hp = export(float, default=100.0)
	defense = export(float, default=0.0)
	player = None #use to store player objects
	knockbacked = Vector2() #set in take_damage and reduce by a rate in each _progress
	velocity = Vector2()
	minrange = 130 #minimum distance until enemy runs away from player
	maxrange = 170 #maximum distance until enemy runs into player
	
	def _ready(self):
		'''runs when object spawn'''
		#prepares require nodes
		self.sprite = self.get_node("AnimatedSprite") #enemy sprite
		self.healthbar = self.get_node("Viewport/HealthBar") #enemy healthbar
	
	def _process(self, delta):
		'''runs every frame'''
		self.movement() #check movement every frames
		
	def movement(self):
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
			
			#if enemy is in the right distance then don't need to move
			if distance in range(self.minrange,self.maxrange):
				return
			
			direction = Vector2(0,0)
			
			#change direction base on whether the player is too close or far
			if distance < self.minrange:
				direction = -(self.player.position - self.position)
			elif distance > self.maxrange:
				direction = (self.player.position - self.position)

			if direction.x < 0: #flip sprite depending on what direction its running to
				self.sprite.flip_h = False
			else:
				self.sprite.flip_h = True

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
	
	
