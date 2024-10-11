from godot import exposed, export
from godot import *


@exposed
class HealButton(Button):

	# member variables here, example:
	player = None


	#THIS BUTTON IS FOR TESTING ONLY, or debug i guess you can use em that way too

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.connect("pressed", self, "on_button_pressed")
		pass
		
	def on_button_pressed(self): #as the event says
		#call function heal in player to heal em
		player = self.get_node("/root/Node2D/Player") #get player node
		player.heal(10)
		
