from godot import exposed, export
from godot import *


@exposed
class ExitButton(Button):

	def _ready(self):
		self.connect("pressed", self, "_on_button_pressed")  # Use underscore prefix
		
	def _on_button_pressed(self):  # Rename method with underscore prefix
		option = self.get_tree().get_root().get_node("/root/Node2D/CanvasLayer/OptionMenu")
		menu = self.get_tree().get_root().get_node("/root/Node2D/CanvasLayer/Menu")
		option.hide()
		menu.show()
		SettingSignal = self.get_tree().get_root().get_node("/root/SettingSignal")
		SettingData = self.get_tree().get_root().get_node("/root/SettingData")
		SettingSignal.update_settings(SettingData.create_storage_dictionary())
