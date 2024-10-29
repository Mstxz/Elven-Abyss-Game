from godot import exposed, export
from godot import *


@exposed
class Loadingscene(Control):

	progress: float = 0.0
	loader: ResourceLoader = None  # Initialize the loader variable

	def _ready(self):
		self.screen_name = "res://scene/Game.tscn"  # Path of scene to load
		self.label = self.get_node("/root/Control/CanvasLayer/Label") 
		self.loader = ResourceLoader.load_interactive(self.screen_name)  # Start loading interactively

	def _process(self, delta):
		if self.loader:
			load_result = self.loader.poll()  # Poll the loading process
			#print("Loading result:", load_result)

		if load_result == OK:
			new_scene = self.loader.get_resource()  # Get the loaded resource
			if new_scene:
				#print("Scene loaded successfully")
				self.get_tree().change_scene_to(new_scene)  # Change to the loaded scene
				self.loader = None  # Clear the loader after loading
	
		elif load_result == ERR_FILE_EOF:
			#print("Reached end of file during loading")
			new_scene = self.loader.get_resource()
			self.get_tree().change_scene_to(new_scene)# Change to the loaded scene
			self.loader = None  
	
		elif load_result != OK:
			#print("Error loading resource")
			self.loader = None  # Clear the loader on error

		# Update loading progress
		stage = self.loader.get_stage()  # Get current loading stage
		stage_count = self.loader.get_stage_count()  # Get total loading stages
		#print("Stage:", stage, "of", stage_count)  # Debug output for future to fix something

		if stage_count > 0:
			self.progress = float(stage) / float(stage_count)
			self.label.text = str(int(self.progress * 100)) + "%"  # Update label text
