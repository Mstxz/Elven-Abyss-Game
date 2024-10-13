from godot import exposed, export
from godot import *


@exposed
class ManaBar(TextureProgress):


	def tweenvalue(self,prop,newvalue):
		#basically automatically change value multiple time to make the illusion of animation
		tween = self.get_node('Tween')
		tween.interpolate_property(
			self,  # Target object
			prop,  # Property to animate
			self.get(prop),  # Start value
			newvalue,  # End value
			0.1,  # Duration in seconds
			Tween.TRANS_LINEAR,  # Transition type
			Tween.EASE_IN_OUT  # Ease type
		)
		tween.start()
	
	def updatemana(self, maxmana, newmana):
		if maxmana == self.max_value: #in case of maxmana changing
			self.tweenvalue('max_value',maxmana)
		self.tweenvalue('value',newmana) #update progress
