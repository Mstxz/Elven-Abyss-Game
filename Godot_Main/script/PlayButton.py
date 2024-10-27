from godot import exposed, export
from godot import *


@exposed
class PlayButton(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		pass
		
	def on_button_pressed(self): #as the event says
		#call function take damage in player to do damage
		self.get_tree().change_scene("res://scene/LoadingScene.tscn")
