from godot import exposed, export
from godot import *


@exposed
class LevelUI(Label):

	# member variables here, example:
	def updateui(self,amount):
		self.text = f'Lv.{amount}'
		
