extends Control

onready var audio_name = $HBoxContainer/Label as Label
onready var audio_num = $HBoxContainer/Label2 as Label
onready var slide = $HBoxContainer/HSlider as HSlider

export(String, "Master", "Music", "Sfx") var bus_name

var bus_index : int = 0

func _ready():
	slide.connect("value_changed", self, "on_value_changed")
	get_bus()
	load_data()
	set_name_label()
	set_slide_value()

func load_data() -> void:
	#load Audio form save file
	match bus_name:
		"Master": 
			on_value_changed(SettingData.get_master_sound())
		"Music":
			on_value_changed(SettingData.get_music_sound())
		"Sfx":
			on_value_changed(SettingData.get_sfx_sound())

func set_name_label() -> void:
	audio_name.text = str(bus_name) + " Volume"

func get_bus() -> void:
	bus_index = AudioServer.get_bus_index(bus_name)

func set_num_label() -> void:
	audio_num.text = str(slide.value * 100)  + "%"

func set_slide_value() -> void:
	slide.value = db2linear(AudioServer.get_bus_volume_db(bus_index))
	set_num_label()

func on_value_changed(value : float) -> void:
	AudioServer.set_bus_volume_db(bus_index, linear2db(value))
	set_num_label()
	
	match bus_index:
		0: 
			SettingSignal.set_master_sound(value)
		1:
			SettingSignal.set_music_sound(value)
		2:
			SettingSignal.set_sfx_sound(value)
