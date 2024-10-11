from godot import exposed, export
from godot import *


@exposed
class ConsumeMana(Button):

	# member variables here, example:
	player = None
	
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
		print('if this return true its mean you have enough mana : ',player.mana_consume(20))
