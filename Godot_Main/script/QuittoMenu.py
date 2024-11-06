from godot import exposed, export
from godot import *

new_scene = ResourceLoader.load("res://scene/MainMenu.tscn")
scene = ResourceLoader.load("res://scene/Loadingscene.tscn")

@exposed
class QuittoMenu(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		self.main = self.get_node("../../../..")
		pass
		
	def on_button_pressed(self): #as the event says
		self.loading = self.get_node("../../../../Loading")
		self.loading.leave()
		self.main.pausesys()
		self.loading.animation.connect("animation_finished", self, "on_animation_finishedd")

	def on_animation_finishedd(self, anim_name):
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		Scenechange.load_main()
