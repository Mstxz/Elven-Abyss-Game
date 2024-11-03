from godot import exposed, export
from godot import *

elemdict = {
	'Water' : Color(0,0.36,1,1),
	'Fire' : Color(1,0.14,0,1),
	'Wind' : Color(0,0.76,0.47,1),
	'Earth' : Color(0.75,0.54,0,1)
}

@exposed
class SkillCd(TextureProgress):


	def tweenvalue(self,prop,start,end,time):
		#basically automatically change value multiple time to make the illusion of animation
		tween = Tween.new()
		self.add_child(tween)
		tween.interpolate_property(
			self,  # Target object
			prop,  # Property to animate
			start,  # Start value
			end,  # End value
			time,  # Duration in seconds
			Tween.TRANS_LINEAR,  # Transition type
			Tween.EASE_IN_OUT  # Ease type
		)
		tween.connect("tween_all_completed",self,"cleartween",Array([tween])) #Clear tween
		if prop == 'value': #connect to showing colored icon func
			tween.connect("tween_all_completed",self,"_on_completed")
		tween.start()
	
	def cleartween(self,tween):
		#Clear tween
		tween.queue_free()

	def activating(self,elem):
		elem = str(elem) #convert gdstr to str
		self.tweenvalue('tint_progress',Color(1,1,1,0.78),elemdict[elem],1)

	def cooldownui(self, time):
		self.tweenvalue('tint_over',Color(1,1,1,1),Color(0,0,0,0),1) #hide colored icon
		self.tweenvalue('tint_progress',self.tint_progress,Color(1,1,1,0.78),1)
		self.max_value = time
		self.value = 0
		self.tweenvalue('value',0,time,time) #update progress
		
	def _on_completed(self):
		#show colored icon
		self.tweenvalue('tint_over',Color(0,0,0,0),Color(1,1,1,1),0.5)
		
