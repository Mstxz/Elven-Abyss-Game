from godot import exposed, export
from godot import *
import random

#put all scenes here
scenes = [
	("res://scene/Stage_R01.tscn", "Stage1"),
	("res://scene/Stage_R02.tscn", "Stage2"),
	("res://scene/Stage_R03.tscn", "Stage3"),
	("res://scene/Shop.tscn", "Shop"),
	#add here below if there's extra
]

@exposed
class ChangeScene(Button):
	#pressed to change scene (God mode)
	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		pass

	def on_button_pressed(self):
		random_scene = random.choice(scenes)
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		Scenechange.load_new(str(random_scene[0]),str(random_scene[1]))
