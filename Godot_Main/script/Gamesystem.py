from godot import exposed, export
from godot import *

pauseload = ResourceLoader.load("res://scene/PauseMenu.tscn")

@exposed
class Gamesystem(Node2D):

	pause = export(bool, default=False)
	
	def _ready(self):
		
		self.pauseMenu = pauseload.instance()
		self.add_child(self.pauseMenu)
		self.canvas = self.get_node('CanvasModulate')
		self.mainui = self.get_node('MainUI')
		self.screenoriginalcolor = self.canvas.color
		self.pauseMenu.hide()

	def _process(self,delta):
		if Input.is_action_just_pressed("pause"):
			self.pausesys()
		if self.pause:
			self.get_tree().set_input_as_handled()

	def pausesys(self):
		self.pause = not self.pause
		if self.pause:
			self.pauseMenu.show()
			self.mainui.hide()
			self.canvas.color = Color(0.1,0.1,0.1,1)
			Engine.time_scale = 0
		else:
			self.pauseMenu.hide()
			self.mainui.show()
			self.canvas.color = self.screenoriginalcolor
			Engine.time_scale = 1
