from godot import exposed, export
from godot import *

@exposed
class Shop(Area2D):

	player_in_area = False
	shop_open = True
	
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
			#appear shop UI
			print('Shop Open')
			self.trigger_shop_ui()
			self.shop_open = True
			
	def trigger_shop_ui(self):
		
		print("Displaying Shop UI")
