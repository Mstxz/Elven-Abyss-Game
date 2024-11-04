from godot import exposed, export
from godot import *


@exposed
class Loadingscene(CanvasLayer):
	
	animation: AnimationPlayer = export(AnimationPlayer)
	
	def _ready(self):
		self.animation = self.get_node("AnimationPlayer")
		self.animation.play("dissolve")

	def leave(self):
		self.animation.play_backwards("dissolve")
