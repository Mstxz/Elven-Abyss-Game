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
	player = None
	player_see = export(bool, default = False)
	
	def _process(self, delta):
		self.runintoplayer()
	
	def runintoplayer(self):
		'''if spot player run into em'''
		if self.player_see:
			direction = self.player.position - self.position
			sprite = self.get_node("AnimatedSprite")
			if direction.x < 0: #flip sprite depending on what direction its running to
				sprite.flip_h = False
			else:
				sprite.flip_h = True
				
			# Normalize direction
			direction = direction.normalized()
			
			# Set velocity based on direction and speed
			self.velocity = direction * self.speed
			
			# Move the enemy using move_and_slide for proper physics handling
			self.move_and_slide(self.velocity)
	
	def _on_Area2D_body_entered(self, body):
		if str(body.name) == "Player":
			self.player = body
			self.player_see = True
		
	def _on_Area2D_body_exited(self, body):
		if str(body.name) == "Player":
			self.player = None
			self.player_see = False
		
	def take_damage(self, dmg):
		self.hp -= dmg
		
	def heal(self, amount):
		self.hp += amount
