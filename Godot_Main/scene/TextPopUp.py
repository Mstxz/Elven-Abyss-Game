from godot import exposed, export
from godot import *


@exposed
class TextPopUp(Area2D):

	def _ready(self):
		# Connect signals and create a timer
		self.connect("body_entered", self, "_on_Area2D_body_entered")
		self.connect("body_exited", self, "_on_Area2D_body_exited")
	
	def _on_Area2D_body_entered(self, body):
		if str(body.name) == "Player":
			tutorial = self.get_node('Tutorial')
			if tutorial:
				self.tweenvalue('self_modulate', Color(1,1,1,1)) #tween
				tutorial.show()
			
	def _on_Area2D_body_exited(self, body):	
		if str(body.name) == "Player":
			tutorial = self.get_node('Tutorial')
			if tutorial:
				self.tweenvalue('self_modulate', Color(1,1,1,0)) #update progress
				
	def tweenvalue(self,prop,newvalue):
		#basically automatically change value multiple time to make the illusion of animation
		tween = self.get_node('Tween')
		target = self.get_node('Tutorial')
		tween.interpolate_property(
			target,  # Target object
			prop,  # Property to animate
			target.get(prop),  # Start value
			newvalue,  # End value
			0.5,  # Duration in seconds
			Tween.TRANS_LINEAR,  # Transition type
			Tween.EASE_IN_OUT  # Ease type
		)
		tween.start()

	
