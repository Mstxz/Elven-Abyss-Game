from godot import exposed, export
from godot import *


@exposed
class LoseMoney(Button):

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.connect("pressed", self, "on_button_pressed")
		pass
		
	def on_button_pressed(self): #as the event says
		#call function take damage in player to do damage
		player = self.get_parent().get_node("../../Player") #get player node
		player.money_modify(-100)
