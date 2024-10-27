from godot import exposed, export
from godot import *

avaliable = ['Water','Fire','Wind','Earth']

@exposed
class ChangeElement(Button):

	def _ready(self):
		#connect press event
		self.connect("pressed", self, "on_button_pressed")
		self.current = 1
		pass
		
	def on_button_pressed(self): #as the event says
		#call function to change the property handled by it own script
		player = self.get_node("/root/Node2D/Player") #get player node
		player.changeelement(avaliable[self.current])
		#change to next
		self.current +=1
		if avaliable[self.current-1] == avaliable[-1]:
			#loop back to first
			self.current = 0
