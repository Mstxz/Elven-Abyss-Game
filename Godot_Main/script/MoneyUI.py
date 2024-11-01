from godot import exposed, export
from godot import *


@exposed
class MoneyUI(Label):

	# member variables here, example:
	def updateui(self,amount):
		self.text = f'$ : {int(amount)}'
