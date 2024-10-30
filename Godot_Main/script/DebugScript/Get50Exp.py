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
		self.player = self.get_node("/root/Node2D/Player") #get player node
		self.expshow = self.get_node("../EXP")
		self.expshow.text = f'EXP : {self.player.exp}'
		pass
	
	def on_button_pressed(self): #as the event says
		self.player.gain_exp(50)
		self.expshow.text = f'EXP : {self.player.exp}'
