from godot import exposed, export
from godot import *


@exposed
class Arrow(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=200.0)
	direction = export(float, default=0.0)
	spawnpos = export(Vector2, default=Vector2(0,0))
	spawnrot = export(float, default=0.0)
	duration = export(float,default=5.0)
	knockback = export(float, default=None)
	damage = export(float,default=10.0)
	target = export(str, default='Player')
	
	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.position = self.spawnpos #As they says
		self.rotation = self.spawnrot
		self.get_node("Timer").start(self.duration)
		pass
		
	def _process(self, delta):
		'''Move toward its direction with set speed and direction'''
		self.velocity = Vector2(-self.speed,0).rotated(self.direction)
		self.move_and_slide(self.velocity)
	
	def _on_Area2D_body_entered(self, body):
		'''Upon hitting the target'''
		if str(self.target) in str(body.name): #check if it is correct target
			#give the knockback max velocity to its target as take_damage param
			#the speed of knockback are to be change
			calculatedknockback = Vector2()
			if not self.knockback:
				calculatedknockback = Vector2(-10,0).rotated(self.direction)
			else:
				calculatedknockback = Vector2(-10*self.knockback,0).rotated(self.direction)
			body.take_damage(self.damage,calculatedknockback)
			self.queue_free() #delete itself after
	
	def _on_Timer_timeout(self):
		'''when the set timer is timed out'''
		self.queue_free()
