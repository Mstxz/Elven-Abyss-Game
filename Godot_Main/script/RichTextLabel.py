from godot import exposed, export
from godot import *


@exposed
class RichTextLabel(RichTextLabel):

	def _ready(self):
		self.SettingData = self.get_tree().get_root().get_node("/root/SettingData")
	
	def _process(self, delta):
		self.text = OS.get_scancode_string(self.SettingData.get_skill_2())
