from godot import exposed, export
from godot import *


@exposed
class SettingButton(Button):

	def _ready(self):
		self.pause = self.get_node("../..")
		self.option = self.get_node("../../../OptionMenu")
		self.connect("pressed", self, "on_button_pressed")
	
	def on_button_pressed(self):
		print(1)
		self.pause.hide()
		self.option.show()
