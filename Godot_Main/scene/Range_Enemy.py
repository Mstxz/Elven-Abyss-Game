from godot import exposed, export
from godot import *


@exposed
class Range_Enemy(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=100.00)
	atk = export(float, default=10.00)
	hp = export(float, default=100.0)
	defense = export(float, default=0.0)
	
	player = None
	player_see = export(bool, default = False) 

	def _process(self, delta):
		if self.player_see:
			direction = -(self.player.position - self.position)
			
			# Normalize direction
			direction = direction.normalized()
			
			# Set velocity based on direction and speed
			self.velocity = direction * self.speed
			
			# Move the enemy using move_and_slide for proper physics handling
			self.move_and_slide(self.velocity)
	
	def _on_Area2D_body_entered(self, body):
		print("end")
		self.player = body
		self.player_see = True
		
	def _on_Area2D_body_exited(self, body):
		self.player = None
		self.player_see = False
