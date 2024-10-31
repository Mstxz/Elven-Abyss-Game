from godot import exposed, export
from godot import Area2D, Input, PackedScene, ResourceLoader, Node

@exposed
class Shop(Area2D):

	player_in_area = False
	shop_open = True

	# Initialize the variable to hold the shop UI scene
	shop_ui_scene = ResourceLoader.load("res://scene/ShopUI.tscn")  
	shop_ui_instance = None  # Keep a reference to the instantiated UI

	def _ready(self):
		# Connect signals
		self.connect("body_entered", self, "_on_Area2D_body_entered")
		self.connect("body_exited", self, "_on_Area2D_body_exited")

	def _on_Area2D_body_entered(self, body):
		print("Enter:", str(body.name), body.filename)
		# Check if the player has entered
		if str(body.name) == "Player":
			print("Player Entered")
			self.player_in_area = True

	def _on_Area2D_body_exited(self, body):
		print("Exit:", body.name)
		# Check if the player has exited
		if str(body.name) == "Player":
			print("Player Exited")
			self.player_in_area = False

	def _process(self, delta):
		# Check if the player is in area and 'F' key is pressed
		if self.player_in_area and Input.is_action_just_pressed("Interact"):
			self.toggle_shop_ui()

	def toggle_shop_ui(self):
		if self.shop_open:
			# If the shop UI is open, close it
			if self.shop_ui_instance is not None:
				self.shop_ui_instance.queue_free()  # Remove it from the scene
				self.shop_ui_instance = None  # Reset the reference
				print("Shop Closed")
			self.shop_open = False
		else:
			# If the shop UI is not open, open it
			if self.shop_ui_scene is not None:
				self.shop_ui_instance = self.shop_ui_scene.instance()
				self.get_tree().current_scene.add_child(self.shop_ui_instance)  # Add to the current scene
				print("Shop Opened")
			self.shop_open = True
