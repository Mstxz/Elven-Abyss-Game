from godot import exposed, export
from godot.bindings import Area2D, Input, ResourceLoader, Timer
import random

@exposed
class InteractableArea(Area2D):
	# List of available stages
	stages = [
		("res://scene/Stage_R01.tscn", "Stage1"),
		("res://scene/Stage_R02.tscn", "Stage2"),
		("res://scene/Stage_R03.tscn", "Stage3"),
		("res://scene/Shop.tscn", "Shop"),
	]
	player_in_area = False
	
	def _ready(self):
		# Connect signals and create a timer
		self.connect("body_entered", self, "_on_Area2D_body_entered")
		self.connect("body_exited", self, "_on_Area2D_body_exited")

	def _on_Area2D_body_entered(self, body):
		print("Enter:",str(body.name), body.filename)
		# Check if the player has entered
		if str(body.name) == "Player":
			print("Player Entered")
			self.player_in_area = True

	def _on_Area2D_body_exited(self, body):
		print("Exit:",body.name)
		# Check if the player has exited
		if str(body.name) == "Player":
			print("Player Exited")
			self.player_in_area = False

	def _process(self, delta):		# Check if the player is in area and 'F' key is pressed
		if self.player_in_area == True and Input.is_action_just_pressed("Interact"):
			random_scene_path = random.choice(self.stages)
			Scenechange = self.get_tree().get_root().get_node("/root/Scenechange")
			Scenechange.load_new(str(random_scene_path[0]),str(random_scene_path[1]))
