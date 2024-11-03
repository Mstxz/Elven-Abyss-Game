extends Control

onready var button = $HBoxContainer/OptionButton as OptionButton

const Resolution_Dictionary : Dictionary = { #create resolution of dict
	"800 x 600" : Vector2(800, 600),
	"1024 x 768" : Vector2(1024, 768),
	"1280 x 720" : Vector2(1280, 720),
	"1280 x 1024" : Vector2(1280, 1024),
	"1366 x 768" : Vector2(1366, 768),
	"1600 x 900" : Vector2(1600, 900),
	"1920 x 1080" : Vector2(1980, 1080)
}

func _ready():
	for i in Resolution_Dictionary: #add button
		button.add_item(i)
	button.connect("item_selected", self, "_on_resolution_selected")

func _on_resolution_selected(index: int) -> void:
	# Turn index to dict key
	var selected_resolution = button.get_item_text(index)
	# Get resolution
	var resolution: Vector2 = Resolution_Dictionary[selected_resolution]
	# set the window size
	OS.window_size = resolution
