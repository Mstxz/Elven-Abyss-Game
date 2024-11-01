from godot import exposed, export
from godot import *


@exposed
class Camera2D(Camera2D):

	player = None

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.player = self.get_node("../Player")
		
		pass
		
	def _process(self, delta):
		
		self.lock_camera(delta)
		
	def lock_camera(self, delta):
		if self.player:
			# Get the player's position
			player_position = self.player.position

			# Lock the camera to the player's position
			self.position = player_position
