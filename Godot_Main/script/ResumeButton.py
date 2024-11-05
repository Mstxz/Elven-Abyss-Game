from godot import exposed, export
from godot import *


@exposed
class ResumeButton(Button):


	def _ready(self):
		self.gameSys = self.get_parent().get_parent().get_parent().get_parent()
		self.connect("pressed", self, "on_button_pressed")
		pass

	def on_button_pressed(self):
		self.gameSys.pausesys()
