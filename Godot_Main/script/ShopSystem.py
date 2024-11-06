from godot import exposed, Array
from godot.bindings import VBoxContainer, Label, Button

@exposed
class Shop(VBoxContainer):
	# Items
	items = {
		"HealthPotion": {"name": "Health Potion", "price": 20},
		"Crossbow": {"name": "Crossbow", "price": 100},
		"Staff": {"name": "Staff", "price": 200}
	}

	item_name_label = None
	price_label = None
	buy_button = None

	# Track the selected item
	selected_item = None

	def _ready(self):
		self.player = self.get_node("/root/Node2D/Player")
		self.item_name_label = self.get_node("../ItemDesc/ItemName")
		self.price_label = self.get_node("../ItemDesc/Prize")
		self.buy_button = self.get_node("../ItemDesc/Buy")

		self.coin = self.player.money

		self.buy_button.disabled = True

		for item_name in self.items.keys():
			button = self.get_node(item_name)
			button.connect("pressed", self, "_on_item_button_pressed", Array([item_name]))
		self.buy_button.connect("pressed", self, "_on_buy_button_pressed")
		
		print("Player:",self.player.money)

	def _on_item_button_pressed(self, item_name):
		"""Handles item button click, shows name and price, and enables buy button."""
		cross = self.get_node("../ItemDesc/Items/Crossbow")
		staff = self.get_node("../ItemDesc/Items/Staff")
		healt = self.get_node("../ItemDesc/Items/HealthPotion")
		if str(item_name) == "Crossbow":
			cross.show()
			staff.hide()
			healt.hide()
		elif str(item_name) == "HealthPotion":
			cross.hide()
			staff.hide()
			healt.show()
		elif str(item_name) == "Staff":
			cross.hide()
			staff.show()
			healt.hide()
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
			self.buy_item(self.selected_item, price, self.coin)
			self.buy_button.disabled = True

	def buy_item(self, item_name, price, player_coin):
		"""Handles the actual purchase,"""
		if str(item_name) == "Crossbow":
			print("Crossbow")
			self.player.changeweapon('Crossbow')
		elif str(item_name) == "HealthPotion":
			print("Health Potion")
			self.player.heal(10)
		elif str(item_name) == "Staff":
			print("Staff")
			self.player.changeweapon('Staff')

		player_coin = -price

		self.player.money_modify(player_coin)
		return player_coin
