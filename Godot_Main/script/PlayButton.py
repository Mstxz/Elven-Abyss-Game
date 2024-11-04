from godot import exposed, export
from godot import *


@exposed
class PlayButton(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		self.loading = self.get_node("../../../Loading")
		pass
		
	def on_button_pressed(self): #as the event says
		self.loading.leave()
		self.loading.animation.connect("animation_finished", self, "on_animation_finished")
		
	def on_animation_finished(self, anim_name):
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		Scenechange.scene = "res://scene/Lobby.tscn"
		Scenechange.new_scene = "Lobby"
		Scenechange.load_game()
