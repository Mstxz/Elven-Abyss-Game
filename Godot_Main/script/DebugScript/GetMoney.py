from godot import exposed, export
from godot import *


@exposed
class GetMoney(Button):

	# member variables here, example:
	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.connect("pressed", self, "on_button_pressed")
		pass
		
	def on_button_pressed(self): #as the event says
		#call function take damage in player to do damage
		player = self.get_node("/root/Node2D/Player") #get player node
		player.money_modify(100)
		