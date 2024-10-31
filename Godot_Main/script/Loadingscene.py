from godot import exposed, export
from godot import *


@exposed
class Loadingscene(Control):

	progress: float = 0.0
	loader : ResourceLoader = None  # Initialize the loader variable
	load = False
	screen_name = export(str, default = "") # Path of scene to load

	def _ready(self):
		Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
		self.screen_name = Scenechange.scene
		Scenechange.scene = ""
		self.label = self.get_node("/root/Control/CanvasLayer/Label")   # Start loading interactively
		self.loader = ResourceLoader.load_interactive(self.screen_name)

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
					self.screen_name = ""
		
			elif load_result == ERR_FILE_EOF:
				#print("Reached end of file during loading")
				self.label.text = str(100) + "%"
				new_scene = self.loader.get_resource()
				self.get_tree().change_scene_to(new_scene)# Change to the loaded scene
				self.loader = None
				self.screen_name = ""
		
			elif load_result != OK:
				#print("Error loading resource")
				self.loader = None  # Clear the loader on error

		if self.loader:
			# Update loading progress
			stage = self.loader.get_stage()  # Get current loading stage
			stage_count = self.loader.get_stage_count()  # Get total loading stages
			#print("Stage:", stage, "of", stage_count)  # Debug output for future to fix something

			if stage_count > 0:
				self.progress = float(stage) / float(stage_count)
				self.label.text = str(int(self.progress * 100)) + "%"  # Update label text
