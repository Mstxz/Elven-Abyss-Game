from godot import exposed, export
from godot import *


@exposed
class EnemyHealthBar(ProgressBar):
	
	def _ready(self):
		self.virtualbar = self.get_parent().get_parent().get_node("VirtualHealthBar")
		pass

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
		
	def updatehealth(self, maxhp, newhp):
		self.virtualbar.visible = True
		if maxhp == self.max_value: #in case of maxhp changing
			self.tweenvalue('max_value', maxhp) #read above function if you wonder what tween is
		self.tweenvalue('value', newhp) #update progress
