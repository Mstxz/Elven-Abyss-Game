from godot import exposed, export
from godot import *


@exposed
class LevelUp(CanvasLayer):

	req = 0
	count = 0
	
	def _ready(self):
		self.PlayerVar = self.get_tree().get_root().get_node("/root/PlayerVar")
		self.exp_label = self.get_node("Panel/Label3")
		self.level_label = self.get_node("Panel/Label2")
	
	def _process(self, delta):
		if not self.req:
			self.req = 48 + (10*self.PlayerVar.level)
		if self.PlayerVar.exp >= self.req:
			self.count += 1
			self.exp_label.text = f"EXP : {self.count}/{self.req}"
			if self.req == self.count:
				self.PlayerVar.exp -= self.req
				self.req = 48 + (10*self.PlayerVar.level)
				self.PlayerVar.level += 1
				self.PlayerVar.skillpoint += 3
				self.count = 0
				self.level_label.text = f"Level : {self.PlayerVar.level}"
				self.exp_label.text = f"EXP : {self.count}/{self.req}"
		else:
			self.count += 1
			if self.count <= self.PlayerVar.exp:
				self.exp_label.text = f"EXP : {self.count}/{self.req}"
				if self.count == self.PlayerVar.exp:
					load = self.get_node("Loading")
					load.leave()
					load.animation.connect("animation_finished", self, "on_animation_finished")
	
	def on_animation_finished(self, anim_name):
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		Scenechange.load_game()
