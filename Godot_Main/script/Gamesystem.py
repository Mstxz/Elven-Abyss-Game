from godot import exposed, export
from godot import *

pauseload = ResourceLoader.load("res://scene/PauseMenu.tscn")
status = ResourceLoader.load("res://scene/StatusUI.tscn")
loading = ResourceLoader.load("res://scene/Loadingscene.tscn")

@exposed
class Gamesystem(Node2D):

	pause = export(bool, default=False)
	is_act = False
	is_stat = False
	
	def _ready(self):
		self.pauseMenu = pauseload.instance()
		self.statusMenu = status.instance()
		self.loading = loading.instance()
		self.add_child(self.loading)
		self.add_child(self.pauseMenu)
		self.add_child(self.statusMenu)
		self.canvas = self.get_node('CanvasModulate')
		self.mainui = self.get_node('MainUI')
		self.screenoriginalcolor = self.canvas.color
		self.pauseMenu.hide()
		self.pausesys(False)
		self.statussys(False)

	def _process(self,delta):
		if not self.is_stat and Input.is_action_just_pressed("pause"):
			self.pausesys()
		elif not self.is_act and Input.is_action_just_pressed("StatusMenu"):
			self.statussys()
			self.get_node("StatusUI").setvar()
		if self.pause:
			self.get_tree().set_input_as_handled()

	def pausesys(self, set = True):
		if set:
			self.pause = not self.pause
		if self.pause:
			self.pauseMenu.show()
			self.mainui.hide()
			self.canvas.color = Color(0.1,0.1,0.1,1)
			Engine.time_scale = 0
			self.is_act = True
		else:
			self.pauseMenu.hide()
			self.mainui.show()
			self.canvas.color = self.screenoriginalcolor
			Engine.time_scale = 1
			self.is_act = False

	def statussys(self, set = True):
		if set:
			self.pause = not self.pause
		if self.pause:
			self.statusMenu.updateplayer()
			self.statusMenu.show()
			self.mainui.hide()
			self.canvas.color = Color(0.1,0.1,0.1,1)
			Engine.time_scale = 0
			self.is_stat = True
		else:
			self.statusMenu.hide()
			self.mainui.show()
			self.canvas.color = self.screenoriginalcolor
			Engine.time_scale = 1
			self.is_stat = False
