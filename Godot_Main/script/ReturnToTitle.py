from godot import exposed, export
from godot import *


@exposed
class ReturnToTitle(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		pass
		
	def on_button_pressed(self): #as the event says
		self.loading = self.get_node("../../../../../Loading")
		self.loading.leave()
		self.loading.animation.connect("animation_finished", self, "on_animation_finishedd")

	def on_animation_finishedd(self, anim_name):
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		Scenechange.scene = "res://scene/MainMenu.tscn"
		Scenechange.new_scene = "Main"
		Scenechange.load_game()
