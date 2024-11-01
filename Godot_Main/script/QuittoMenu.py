from godot import exposed, export
from godot import *

new_scene = ResourceLoader.load("res://scene/MainMenu.tscn")
scene = ResourceLoader.load("res://scene/Loadingscene.tscn")

@exposed
class QuittoMenu(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		pass
		
	def on_button_pressed(self): #as the event says
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		Scenechange.scene = "res://scene/MainMenu.tscn"
		Scenechange.new_scene = "Main"
		Scenechange.load()
