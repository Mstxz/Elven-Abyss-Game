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
	velocity = Vector2()

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
		# Get input axis for horizontal movement
		direction_x = Input.get_axis("left", "right")
		direction_y = Input.get_axis("up", "down")
		
		if direction_x or direction_y:
			self.velocity.x = direction_x * self.speed
			self.velocity.y = direction_y * self.speed
			#if direction_x or (direction_x and direction_y):
				#self.sprite.play("run_l")

			if direction_x < 0:
				self.sprite.flip_h = False

			elif direction_x > 0:
				self.sprite.flip_h = True
			
			#elif direction_y > 0:
				#self.sprite.play("run_d")
			#elif direction_y < 0:
				#self.sprite.play("run_u")
				
		else:
			self.velocity.x = 0
			self.velocity.y = 0  # Stop moving when there's no input
			self.sprite.flip_h = False
			#self.sprite.play("default")
		# Move the KinematicBody2D
		self.velocity = self.move_and_slide(self.velocity)
		
	def take_damage(self, dmg):
		self.hp -= dmg
		
	def heal(self, amount):
		self.hp += amount
