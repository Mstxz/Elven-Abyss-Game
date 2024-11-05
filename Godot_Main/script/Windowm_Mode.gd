extends Control

onready var button = $HBoxContainer/OptionButton as OptionButton

const Window_Mode_Array : Array = [ #create list of window mode
	"Window Mode",
	"Fullscreen",
	"Borderless Window",
	"Borderless Fullscreen"
]

func _ready():
	# Add button
	for mode in Window_Mode_Array:
		button.add_item(mode)

	button.connect("item_selected", self, "_on_window_mode_selected")
	load_data()

func load_data() -> void:
	#load Window mode form save file
	_on_window_mode_selected(SettingData.get_window_mode_index())
	button.select(SettingData.get_window_mode_index())

func _on_window_mode_selected(index: int) -> void:
	SettingSignal.select_window_mode(index)
	match index:
		0:  # Window Mode
			OS.window_fullscreen = false
			OS.window_borderless = false
		1: # Fullscreen
			OS.window_fullscreen = true
			OS.window_borderless = false
		2:  # Borderless Window
			OS.window_fullscreen = false
			OS.window_borderless = true
		3:  # Borderless Fullscreen
			OS.window_fullscreen = true
			OS.window_borderless = true
