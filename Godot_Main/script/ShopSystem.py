from godot import exposed, Array
from godot.bindings import VBoxContainer, Label, Button

@exposed
class Shop(VBoxContainer):
	# Items
	items = {
		"HealthPotion": {"name": "Health Potion", "price": 10},
		"Bow": {"name": "Bow", "price": 20},
		"Sword": {"name": "Sword", "price": 30},
		"Staff": {"name": "Staff", "price": 40}
	}

	item_name_label = None
	price_label = None
	buy_button = None

	# Track the selected item
	selected_item = None

	def _ready(self):
		self.item_name_label = self.get_node("../ItemDesc/ItemName")
		self.price_label = self.get_node("../ItemDesc/Prize")
		self.buy_button = self.get_node("../ItemDesc/Buy")

		self.buy_button.disabled = True

		for item_name in self.items.keys():
			button = self.get_node(item_name)
			button.connect("pressed", self, "_on_item_button_pressed", Array([item_name]))
		self.buy_button.connect("pressed", self, "_on_buy_button_pressed")

	def _on_item_button_pressed(self, item_name):
		"""Handles item button click, shows name and price, and enables buy button."""
		self.selected_item = item_name
		item_info = self.items[str(item_name)]

		#Display Item
		self.item_name_label.text = item_info['name']
		self.price_label.text = f"Price: {item_info['price']}"
		self.buy_button.disabled = False

	def _on_buy_button_pressed(self):
		"""Handles buying logic when the buy button is clicked."""
		if self.selected_item:
			item_info = self.items[str(self.selected_item)]
			price = item_info["price"]

			if self.player_can_afford(price):
				self.buy_item(self.selected_item, price)
				self.buy_button.disabled = True
			else:
				print("Fron ShopSystem: Player Cannot Buy")

	def player_can_afford(self, price):
		"""Placeholder for checking if the player has enough currency."""
		return True  # Assuming player can afford for now

	def buy_item(self, item_name, price):
		"""Handles the actual purchase,"""
		pass
