from godot import exposed, export
from godot import *

scene = ResourceLoader.load("res://scene/Loadingscene.tscn")


@exposed
class PlayButton(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		pass
		
	def on_button_pressed(self): #as the event says
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		Scenechange.scene = "res://scene/Lobby.tscn"
		Scenechange.new_scene = "Lobby"
		Scenechange.load()
