from godot import exposed, export
from godot import *

loading = ResourceLoader.load("res://scene/Loadingscene.tscn", "", True)

@exposed
class Scenechange(Node):

	scene = export(str, default="") # scene for loading script example res://...
	new_scene = export(str, default="") # scene that want to go by name example "Main" and "Game" in menu everytime that load new scene create name and assign it in namee
	namee = {} #store loaded scene load only one time and can use everytime
	last_scene = export(str, default="res://scene/Game.tscn") #make for future now it not important

	def _ready(self):
		# LoadScene that want to use when open game
		mainmenu = ResourceLoader.load("res://scene/MainMenu.tscn", "", True)
		game = ResourceLoader.load(self.last_scene, "", True)
		# store loaded scene in dict
		self.namee["Main"] = mainmenu
		self.namee["Game"] = game

	def change_scene(self, scene: PackedScene):
		"""Change scene system"""
		# Delete current scene
		self.get_parent().get_child(2).queue_free()
		# Instance the new scene and add it to the current scene tree
		self.current_scene = scene.instance()
		self.get_tree().root.call_deferred("add_child", self.current_scene)

	def load_game(self):
		"""Load the game scene and change to it"""
		self.change_scene(self.namee[str(self.new_scene)])
		
	def load(self):
		"""Load the loading scene"""
		self.change_scene(loading)

	def load_new(self, filepath, sname):
		"""Use for load new scene that not assign in this script"""
		self.last_scene = str(filepath) #future
		self.scene = str(filepath) #for loading scene script
		self.new_scene = str(sname) #new scene name
		if sname not in self.namee:
			#if this scene didn't load before, load it
			game = ResourceLoader.load(self.last_scene, "", True)
			self.namee[str(sname)] = game
		self.load()
