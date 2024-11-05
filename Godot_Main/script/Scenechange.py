from godot import exposed, export
from godot import *

@exposed
class Scenechange(Node):

	scene = export(str, default="") # scene for loading script example res://...
	new_scene = export(str, default="") # scene that want to go by name example "Main" and "Game" in menu everytime that load new scene create name and assign it in namee
	namee = {} #store loaded scene load only one time and can use everytime
	last_scene = export(str, default="res://scene/Lobby.tscn") #make for future now it not important

	def _ready(self):
		# LoadScene that want to use when open game
		mainmenu = ResourceLoader.load("res://scene/MainMenu.tscn", "", True)
		game = ResourceLoader.load(self.last_scene, "", True)
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
		self.change_scene(self.namee[str(self.new_scene)])

	def load_new(self, filepath, sname):
		"""Use for load new scene that not assign in this script"""
		self.last_scene = str(filepath) #future
		self.scene = str(filepath) #for loading scene script
		self.new_scene = str(sname) #new scene name
		if sname not in self.namee:
			#if this scene didn't load before, load it
			game = ResourceLoader.load(self.last_scene, "", True)
			self.namee[str(sname)] = game
		self.load_game()
	
	def find_first_child_of_class(self, parent, classname=Node2D):
		for child in parent.get_children():
			if isinstance(child,classname):
				return child
		return None  # Return None if no child of the specified class is found
