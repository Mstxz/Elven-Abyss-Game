"""Player System"""
from godot import exposed, export
from godot import *

@exposed
class Player(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=150.0)
	atk = export(float, default=10.00)
	hp = export(float, default=100.0)
	exp = export(int, default=0)
	mana = export(float, default=100.0)
	defense = export(float, default=0.0)
	critrate = export(float, default=0.0)
	critdmg = export(float, default=50.0)

	def _ready(self):
		"""
		Called when the node is added to the scene.
		Initialization happens here.
		"""
		self.sprite = self.get_node("AnimatedSprite")
		pass

	def _process(self, delta):
		"""
		Called every frame. Use it for real-time input handling.
		"""
		self.move(delta)

	def move(self, delta):
		"""Player Movement"""
		direction_x = Input.get_axis("ui_left", "ui_right")
		direction_y = Input.get_axis("ui_up", "ui_down")
		velocity = Vector2(direction_x, direction_y)
		
		if velocity.length() > 0:
			velocity = velocity.normalized()
			
		
		self.move_and_slide(velocity * self.speed)

	def take_damage(self, dmg):
		self.hp -= dmg

	def heal(self, amount):
		self.hp += amount
