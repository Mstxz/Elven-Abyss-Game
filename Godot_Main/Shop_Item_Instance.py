# shop_stand.py
from godot import Node2D, Area2D, Signal
from item import Item
import random

class Shop_Itrm_Instance(Node2D):

	items = [
		Item("res://assets/Kyrises_16x16_RPG_Icon_Pack_V1.3/Kyrise's 16x16 RPG Icon Pack - V1.3/icons/16x16/potion_02a.png"),
		Item("res://assets/Kyrises_16x16_RPG_Icon_Pack_V1.3/Kyrise's 16x16 RPG Icon Pack - V1.3/icons/16x16/bow_02a.png"),
		Item("res://assets/Kyrises_16x16_RPG_Icon_Pack_V1.3/Kyrise's 16x16 RPG Icon Pack - V1.3/icons/16x16/staff_03a.png"),
		Item("res://assets/Kyrises_16x16_RPG_Icon_Pack_V1.3/Kyrise's 16x16 RPG Icon Pack - V1.3/icons/16x16/sword_02a.png")
	]

	def _ready(self):
		# Connect the Area2D's body_entered signal to the method
		self.get_node("Area2D").connect("body_entered", self, "_on_player_entered")

	def _on_player_entered(self, body):
		# Ensure the body is the player or any specific condition you want
		if str(body.name) == "Player":  # Assuming the player is added to this group
			self.change_potion()

	def change_potion(self):
		random_index = random.randint(0, len(self.items) - 1)  # Get a random index
		self.get_node("Potion").texture = self.items[random_index].texture  # Change the potion texture
