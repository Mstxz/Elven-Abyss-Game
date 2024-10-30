from godot import exposed, export
from godot import *


@exposed
class Scenechange(Node):

	# member variables here, example:
	scene = export(str, default="")

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass
