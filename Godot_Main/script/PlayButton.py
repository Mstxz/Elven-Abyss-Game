from godot import exposed, export
from godot import *


@exposed
class PlayButton(Button):

	def _ready(self):
		self.connect("pressed", self, "on_button_pressed")
		self.connect("mouse_entered", self, "on_mouse_entered")
		self.loading = self.get_node("../../../Loading")
		self.PlayerVar = self.get_tree().get_root().get_node("/root/PlayerVar")
		self.updatevar()
		pass
		
	def on_button_pressed(self): #as the event says
		self.loading.leave()
		self.loading.animation.connect("animation_finished", self, "on_animation_finished")
		
	def on_animation_finished(self, anim_name):
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		Scenechange.scene = "res://scene/Lobby.tscn"
		Scenechange.new_scene = "Lobby"
		Scenechange.load_game()
		
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
		self.PlayerVar.element = "Water"
		self.PlayerVar.skillpoint = 0
	
	def on_mouse_entered(self):
		self.get_node("HoverSfx").play()
