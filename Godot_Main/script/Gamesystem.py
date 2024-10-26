from godot import exposed, export
from godot import *


@exposed
class Gamesystem(Node2D):

	pause = export(bool, default=False)

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.pauseMenu = self.get_node("/root/Node2D/PauseMenu")
		self.pauseMenu.hide()

	def _process(self,delta):
		if Input.is_action_just_pressed("pause"):
			self.pausesys()
		if self.pause:
			self.get_tree().set_input_as_handled()

	def pausesys(self):
		self.pause = not self.pause
		if self.pause:
			self.pauseMenu.show()
			Engine.time_scale = 0
		else:
			self.pauseMenu.hide()
			Engine.time_scale = 1
