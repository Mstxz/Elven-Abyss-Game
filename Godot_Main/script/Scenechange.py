from godot import exposed, export
from godot import *


@exposed
class Scenechange(Node):

	# member variables here, example:
	scene = export(str, default="")
	scene_to_load: PackedScene = export(PackedScene)
	new_scene: PackedScene = export(PackedScene)
	
	def _ready(self):
		self.scene_to_load = ResourceLoader.load("res://scene/Loadingscene.tscn")

	def load(self):
		self.new_scene = ResourceLoader.load(self.scene)
