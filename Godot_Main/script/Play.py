from godot import exposed, export
from godot import *


@exposed
class Play(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		self.connect("mouse_entered", self, "on_mouse_entered")
		pass
		
	
		
	def on_button_pressed(self): #as the event says
		element = self.get_tree().get_root().get_child(5).get_node("CanvasLayer/CanvasLayer2")
		menu = self.get_tree().get_root().get_child(5).get_node("CanvasLayer/Menu")
		element.show()
		menu.hide()
	
	def on_mouse_entered(self):
		self.get_node("HoverSfx").play()
