from godot import exposed, export
from godot import *


@exposed
class QuitGameButton(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		self.connect("mouse_entered", self, "on_mouse_entered")
		pass
		
	def on_button_pressed(self): #as the event says
		#call function take damage in player to do damage
		self.get_tree().quit()


	def on_mouse_entered(self):
		self.get_node("HoverSfx").play()
