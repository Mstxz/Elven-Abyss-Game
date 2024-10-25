from godot import exposed, export
from godot import *


@exposed
class Get50Exp(Button):

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
		player.gain_exp(50)
		expshow = self.get_node("../EXP")
		expshow.text = f'EXP : {player.exp}'
