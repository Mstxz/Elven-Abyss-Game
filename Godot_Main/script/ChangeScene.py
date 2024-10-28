from godot import exposed, export
from godot import *
import random

#put all scenes here
scenes = [
	"res://scene/Stage_R01.tscn",
	"res://scene/Stage_R02.tscn",
	"res://scene/Stage_R03.tscn",
]

@exposed
class ChangeScene(Button):
	#pressed to change scene (God mode)
	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		pass
		
	def on_button_pressed(self):
		random_scene = random.choice(scenes)
		self.get_tree().change_scene(random_scene) #make this random
