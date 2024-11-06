from godot import exposed, export
from godot import *

loading = ResourceLoader.load("res://scene/LevelUp.tscn", "", True)
shop = ResourceLoader.load("res://scene/Shop.tscn", "", True)
boss = ResourceLoader.load("res://scene/Stage_Boss.tscn", "", True)

@exposed
class Scenechange(Node):

	scene = export(str, default="") # scene for loading script example res://...
	new_scene = export(str, default="") # scene that want to go by name example "Main" and "Game" in menu everytime that load new scene create name and assign it in namee
	namee = {} #store loaded scene load only one time and can use everytime
	last_scene = export(str, default="Lobby") #make for future now it not important
	map_lim = export(int, default = 5)
	count = 0
	count_shop = 1

	def _ready(self):
		# LoadScene that want to use when open game
		mainmenu = ResourceLoader.load("res://scene/MainMenu.tscn", "", True)
		game = ResourceLoader.load("res://scene/Lobby.tscn", "", True)
		# store loaded scene in dict
		self.namee["Main"] = mainmenu
		self.namee["Lobby"] = game

	def change_scene(self, scene: PackedScene):
		"""Change scene system"""
		# Delete current scene
		canva = self.find_first_child_of_class(self.get_parent().get_child(5), CanvasModulate)
		if canva:
			self.get_parent().get_child(5).remove_child(canva)
		self.get_parent().get_child(5).queue_free()
		# Instance the new scene and add it to the current scene tree
		self.current_scene = scene.instance()
		self.get_tree().root.call_deferred("add_child", self.current_scene)

	def load_game(self):
		"""Load the game scene and change to it"""
		if not self.count_shop:
			self.change_scene(shop)
			self.count_shop = 2
			self.last_scene = shop
		elif self.count == self.map_lim:
			self.change_scene(boss)
			self.last_scene = boss
		else:
			self.count_shop -= 1
			self.count += 1
			self.change_scene(self.namee[str(self.new_scene)])
			self.last_scene = self.new_scene
	
	def load_last(self):
		self.change_scene(self.namee[str(self.last_scene)])
	
	def load_main(self):
		self.change_scene(self.namee["Main"])
	
	def load_new_game(self):
		self.change_scene(self.namee["Lobby"])
	
	def load(self):
		"""Load the game scene and change to it"""
		PlayerVar = self.get_tree().get_root().get_node("/root/PlayerVar")
		req = 48 + (10*PlayerVar.level)
		if PlayerVar.exp >= req:
			self.change_scene(loading)
		else:
			self.load_game()

	def load_new(self, filepath, sname):
		"""Use for load new scene that not assign in this script"""
		self.scene = str(filepath) #for loading scene script
		self.new_scene = str(sname) #new scene name
		self.last_scene = self.new_scene
		if sname not in self.namee:
			#if this scene didn't load before, load it
			game = ResourceLoader.load(self.scene, "", True)
			self.namee[str(sname)] = game
		self.load()
	
	def find_first_child_of_class(self, parent, classname=Node2D):
		for child in parent.get_children():
			if isinstance(child,classname):
				return child
		return None  # Return None if no child of the specified class is found
