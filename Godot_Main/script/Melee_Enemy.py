from godot import exposed, export
from godot import *


@exposed
class Melee_Enemy(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=60.0)
	atk = export(float, default=10.00)
	maxhp = export(float, default=100.0)
	hp = export(float, default=100.0)
	defense = export(float, default=0.0)
	player = None #use to store player object
	knockbacked = Vector2() #set in take_damage and reduce by a rate in each _progress
	velocity = Vector2()
	is_timer = False
	timer = 0.0
	delay = 2.0
	
	def _ready(self):
		'''runs when object spawn'''
		#prepares require nodes
		
		self.sprite = self.get_node("AnimatedSprite") #enemy sprite
		self.healthbar = self.get_node("Viewport/HealthBar") #enemy healthbar
		self.hitbox = self.get_node("Hitbox")
	
	def _process(self, delta):
		'''runs every frame'''
		self.movement(delta) #check movement every frames
		
	def movement(self, delta):
		'''handle all kind of enemy movement'''
		if abs(self.knockbacked.x) + abs(self.knockbacked.y) > 5:
			# in case theres no player in range and theres still kb
			# so this have to be outside main if
			self.velocity *= 0.9
			self.knockbacked *= 0.9
			if not self.player:
				# Move the enemy using move_and_slide for proper physics handling
				self.move_and_slide(self.velocity)
		
		if self.player: #if there is player in sight:
				#get direction
				direction = self.player.position - self.position
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
				#check if the player too far walk
				if self.player.position.distance_to(self.position) > 40:
				# Move the enemy using move_and_slide for proper physics handling
					self.move_and_slide(self.velocity)
				#check if the player close enouge attack !!
				else:
					#change position to left or right of player
					direction = Vector2(self.position.x - self.player.position.x,self.player.position.y - self.position.y)
					direction = direction.normalized()
					self.velocity = direction * self.speed
					self.move_and_slide(self.velocity)
					self.attack(delta)

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
		print("enter")
		if str(body.name) == "Player": #prevent recognizing other kinematic2d
			self.player.take_damage(self.atk) 
	
	def _on_Hitbox_body_exited(self, body):
		'''player will tkae damage when enter area'''
		print("exit")

	def hitbox_change(self,delta):
		'''change hitbox position to deal damage to player'''
		if not self.is_timer:
			direction = self.player.position - self.position
			if direction.x < 0:
				self.hitbox.position = Vector2(-20,0) #change hitbox position
			else:
				self.hitbox.position = Vector2(20,0) #change hitbox position
			#make delay attack
			self.timer += delta
			if self.timer >= self.delay: #make hitbox back to default when finish timer
				self.hitbox.position = Vector2(0,0)
				self.timer = 0.0
				self.is_timer = True #loop timer
		else:
			self.timer += delta
			if self.timer >= self.delay: #make timer delay before another loop
				self.timer = 0.0
				self.is_timer = False #loop timer

	def attack(self,delta):
		'''attack function'''
		self.hitbox_change(delta)

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
