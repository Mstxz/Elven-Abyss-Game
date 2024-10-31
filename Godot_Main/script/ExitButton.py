from godot import exposed, export
from godot import *


@exposed
class ExitButton(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		pass
		
	def on_button_pressed(self): #as the event says
		option = self.get_tree().get_root().get_node("/root/Node2D/CanvasLayer/OptionMenu")
		menu = self.get_tree().get_root().get_node("/root/Node2D/CanvasLayer/Menu")
		option.hide()
		menu.show()
