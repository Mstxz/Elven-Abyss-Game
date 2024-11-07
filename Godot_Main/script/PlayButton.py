from godot import exposed, export
from godot import *

elemdict = {
	'Water' : Color(0,0.36,1,1),
	'Fire' : Color(1,0.14,0,1),
	'Wind' : Color(0,0.76,0.47,1),
	'Earth' : Color(0.75,0.54,0,1)
}

@exposed
class PlayButton(Button):
	
	element = export(str, default='Water')
	
	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		self.connect("mouse_entered", self, "on_mouse_entered")
		self.connect("mouse_exited", self, "on_mouse_exit")
		self.loading = self.get_node("../../../Loading")
		self.PlayerVar = self.get_tree().get_root().get_node("/root/PlayerVar")
		pass
		
	def on_button_pressed(self): #as the event says
		self.updatevar()
		self.loading.leave()
		self.loading.animation.connect("animation_finished", self, "on_animation_finished")
		
	def on_animation_finished(self, anim_name):
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		Scenechange.load_new_game()
		
	def updatevar(self):
		'''update player var to global'''
		self.PlayerVar.speed = 150.0
		self.PlayerVar.atk = 10.0
		self.PlayerVar.maxhp = 100.0
		self.PlayerVar.hp = 100.0
		self.PlayerVar.level = 1
		self.PlayerVar.exp = 0.0
		self.PlayerVar.money = 100
		self.PlayerVar.maxmana = 100.0
		self.PlayerVar.mana = 100.0
		self.PlayerVar.defense = 0.0
		self.PlayerVar.critrate = 0.0
		self.PlayerVar.critdmg = 50.0
		self.PlayerVar.weapon = 'Stick'
		self.PlayerVar.element = self.element
		print(self.element)
		self.PlayerVar.skillpoint = 0
	
	def on_mouse_entered(self):
		self.get_node("HoverSfx").play()
		self.tweenvalue('modulate',Color(1,1,1,1),elemdict[str(self.element)],0.1)
	
	def on_mouse_exit(self):
		self.tweenvalue('modulate',elemdict[str(self.element)],Color(1,1,1,1),0.1)
	
	def tweenvalue(self,prop,start,end,time):
		#basically automatically change value multiple time to make the illusion of animation
		tween = self.get_node('Tween')
		tween.interpolate_property(
			self,  # Target object
			prop,  # Property to animate
			start,  # Start value
			end,  # End value
			time,  # Duration in seconds
			Tween.TRANS_LINEAR,  # Transition type
			Tween.EASE_IN_OUT  # Ease type
		)
		if prop == 'value': #connect to showing colored icon func
			tween.connect("tween_all_completed",self,"_on_completed")
		tween.start()
