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
	player = None
	knockbacked = Vector2() #set in take_damage and reduce by a rate in each _progress
	velocity = Vector2()
	minrange = 130
	maxrange = 170

	def _process(self, delta):
		self.movement()
		
	def movement(self):
		if abs(self.knockbacked.x) + abs(self.knockbacked.y) > 5:
			# in case theres no player in range and theres still kb
			# so this have to be outside main if
			self.velocity *= 0.9
			self.knockbacked *= 0.9
			if not self.player:
				# Move the enemy using move_and_slide for proper physics handling
				self.move_and_slide(self.velocity)
		
		if self.player:
			distance = self.player.position.distance_to(self.position)
			if distance in range(self.minrange,self.maxrange):
				return
			direction = Vector2(0,0)
			if distance < self.minrange:
				direction = -(self.player.position - self.position)
			elif distance > self.maxrange:
				direction = (self.player.position - self.position)
			sprite = self.get_node("AnimatedSprite")
			if direction.x < 0: #flip sprite depending on what direction its running to
				sprite.flip_h = False
			else:
				sprite.flip_h = True

			# Normalize direction
			direction = direction.normalized()
			
			# If the knockbacked are not reduced enough do not move
			# or else it would set the velocity thus ends the knockback
			if abs(self.knockbacked.x) + abs(self.knockbacked.y) < 5:
				# if knockback is reduced enough back to walking
				self.velocity = direction * self.speed
				self.knockbacked *= 0
			
			
			# Move the enemy using move_and_slide for proper physics handling
			self.move_and_slide(self.velocity)
			
	def _on_Area2D_body_entered(self, body):
		if str(body.name) == "Player":
			self.player = body
		
	def _on_Area2D_body_exited(self, body):
		if str(body.name) == "Player":
			self.player = None
		
	def death(self):
		self.queue_free()
	
	def hp_changed_func(self):
		healthbar = self.get_node("Viewport/HealthBar")
		healthbar.updatehealth(self.maxhp,self.hp)
	
	def take_damage(self, dmg, kb=None):
		dmg = max(dmg-self.defense, 1) #reduce damage with defense with the least possible dmg is 1
		dmg = min(self.hp,dmg)
		if kb:
			self.velocity = kb
			self.knockbacked = kb
			self.move_and_slide(self.velocity)
		if dmg:
			self.hp -= dmg
			self.hp_changed_func()
		if self.hp <= 0:
			self.death()
		
	def heal(self, amount):
		self.hp += amount
	
	
