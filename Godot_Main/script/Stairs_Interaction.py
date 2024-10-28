from godot import exposed, export
from godot.bindings import Area2D, Input, ResourceLoader, Timer
import random

@exposed
class InteractableArea(Area2D):
	# List of available stages
	stages = [
		"res://scene/Stage_R01.tscn",
		"res://scene/Stage_R02.tscn",
		"res://scene/Stage_R03.tscn",
	]
	# Path to the loading scene
	loading_scene_path = "res://scene/Loadingscene.tscn"
	
	player_in_area = False
	timer = None  # Timer for delay before switching to random scene

	def _ready(self):
		# Connect signals and create a timer
		self.connect("body_entered", self, "_on_Area2D_body_entered")
		self.connect("body_exited", self, "_on_Area2D_body_exited")
		
		# Add and configure the timer
		self.timer = Timer.new()
		self.timer.set_wait_time(2)  # 2 seconds delay (adjust as needed)
		self.timer.set_one_shot(True)
		self.timer.connect("timeout", self, "_on_timer_timeout")
		self.add_child(self.timer)

	def _on_Area2D_body_entered(self, body):
		# Check if the player has entered
		if body.name == "Player":
			self.player_in_area = True

	def _on_Area2D_body_exited(self, body):
		# Check if the player has exited
		if body.name == "Player":
			self.player_in_area = False

	def _process(self, delta):
		# Check if the player is in area and 'F' key is pressed
		if self.player_in_area and Input.is_action_just_pressed("Interact"):
			self.load_loading_scene()
			print('Interacted')

	def load_loading_scene(self):
		# Load and transition to the loading scene
		loading_scene = ResourceLoader.load(self.loading_scene_path)
		if loading_scene:
			self.get_tree().change_scene_to(loading_scene)
			# Start the timer for transitioning to the random scene
			self.timer.start()
		else:
			print("Error: Could not load loading scene.")

	def _on_timer_timeout(self):
		# Select a random scene from the list and transition to it
		random_scene_path = random.choice(self.stages)
		random_scene = ResourceLoader.load(random_scene_path)
		if random_scene:
			self.get_tree().change_scene_to(random_scene)
		else:
			print("Error: Could not load random scene.")
