extends Node


var window_mode_index : int = 0
var window_res_index : int = 0
var master_sound : float = 0.0
var music_sound : float = 0.0
var sfx_sound : float = 0.0
var loaded_data : Dictionary = {}

func _ready():
	handle_signal()
	create_storage_dictionary()

func create_storage_dictionary() -> Dictionary:
	#create a dict that store all setting
	var setting_container_dict: Dictionary = {
		"window_mode_index" : window_mode_index,
		"window_res_index" : window_res_index,
		"master_sound" : master_sound,
		"music_sound" : music_sound,
		"sfx_sound" : sfx_sound,
	}
	return setting_container_dict

func get_window_mode_index() -> int:
	if loaded_data == {}:
		return 0
	return window_mode_index

func get_window_res_index() -> int:
	if loaded_data == {}:
		return 0
	return window_res_index

func get_master_sound() -> float:
	if loaded_data == {}:
		return 1.0
	return master_sound

func get_music_sound() -> float:
	if loaded_data == {}:
		return 1.0
	return music_sound

func get_sfx_sound() -> float:
	if loaded_data == {}:
		return 1.0
	return sfx_sound

func on_window_mode_selected(index: int) -> void:
	# update value when trigger signal
	window_mode_index = index

func on_window_res_selected(index: int) -> void:
	# update value when trigger signal
	window_res_index = index

func on_master_sound_set(value: float) -> void:
	# update value when trigger signal
	master_sound = value

func on_music_sound_set(value: float) -> void:
	# update value when trigger signal
	music_sound = value

func on_sfx_sound_set(value: float) -> void:
	# update value when trigger signal
	sfx_sound = value

func on_load_setting_data(data: Dictionary) -> void:
	# update value when trigger signal
	loaded_data = data
	on_window_mode_selected(loaded_data.window_mode_index)
	on_window_res_selected(loaded_data.window_res_index)
	on_master_sound_set(loaded_data.master_sound)
	on_music_sound_set(loaded_data.music_sound)
	on_sfx_sound_set(loaded_data.sfx_sound)
	

func handle_signal() -> void:
	# connect signal
	SettingSignal.connect("on_window_mode_selected", self, "on_window_mode_selected")
	SettingSignal.connect("on_window_res_selected", self, "on_window_res_selected")
	SettingSignal.connect("on_master_sound_set", self, "on_master_sound_set")
	SettingSignal.connect("on_music_sound_set", self, "on_music_sound_set")
	SettingSignal.connect("on_sfx_sound_set", self, "on_sfx_sound_set")
	SettingSignal.connect("load_setting_data", self, "on_load_setting_data")
