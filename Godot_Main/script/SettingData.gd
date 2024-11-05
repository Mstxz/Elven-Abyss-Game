extends Node


var window_mode_index : int = 1
var window_res_index : int = 6
var master_sound : float = 1.0
var music_sound : float = 1.0
var sfx_sound : float = 1.0
var loaded_data : Dictionary = {}
var left : int = InputMap.get_action_list("left")[0].scancode
var right : int = InputMap.get_action_list("right")[0].scancode
var up : int = InputMap.get_action_list("up")[0].scancode
var down : int = InputMap.get_action_list("down")[0].scancode
var skill1 : int = InputMap.get_action_list("skill1")[0].scancode
var skill2 : int = InputMap.get_action_list("skill2")[0].scancode
var Interact : int = InputMap.get_action_list("Interact")[0].scancode

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
		"left": left,
		"right": right,
		"up": up,
		"down": down,
		"skill1": skill1,
		"skill2": skill2,
		"Interact": Interact
	}
	return setting_container_dict

func get_window_mode_index() -> int:
	return window_mode_index

func get_window_res_index() -> int:
	return window_res_index

func get_master_sound() -> float:
	return master_sound

func get_music_sound() -> float:
	return music_sound

func get_sfx_sound() -> float:
	return sfx_sound

func get_left() -> int:
	return left

func get_right() -> int:
	return right

func get_up() -> int:
	return up

func get_down() -> int:
	return down

func get_skill_1() -> int:
	return skill1

func get_skill_2() -> int:
	return skill2

func get_interact() -> int:
	return Interact

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

func on_left_key_set(array: int) -> void:
	# update value when trigger signal
	left = array

func on_right_key_set(array: int) -> void:
	# update value when trigger signal
	right = array

func on_up_key_set(array: int) -> void:
	# update value when trigger signal
	up = array

func on_down_key_set(array: int) -> void:
	# update value when trigger signal
	down = array

func on_skill_1_set(array: int) -> void:
	# update value when trigger signal
	skill1 = array

func on_skill_2_set(array: int) -> void:
	# update value when trigger signal
	skill2 = array

func on_interact_set(array: int) -> void:
	# update value when trigger signal
	Interact = array

func on_load_setting_data(data: Dictionary) -> void:
	# update value when trigger signal
	loaded_data = data
	print(loaded_data.up)
	on_window_mode_selected(loaded_data.window_mode_index)
	on_window_res_selected(loaded_data.window_res_index)
	on_master_sound_set(loaded_data.master_sound)
	on_music_sound_set(loaded_data.music_sound)
	on_sfx_sound_set(loaded_data.sfx_sound)
	on_left_key_set(loaded_data.left)
	on_right_key_set(loaded_data.right)
	on_up_key_set(loaded_data.up)
	on_down_key_set(loaded_data.down)
	on_skill_1_set(loaded_data.skill1)
	on_skill_2_set(loaded_data.skill2)
	on_interact_set(loaded_data.Interact)

func handle_signal() -> void:
	# connect signal
	SettingSignal.connect("on_window_mode_selected", self, "on_window_mode_selected")
	SettingSignal.connect("on_window_res_selected", self, "on_window_res_selected")
	SettingSignal.connect("on_master_sound_set", self, "on_master_sound_set")
	SettingSignal.connect("on_music_sound_set", self, "on_music_sound_set")
	SettingSignal.connect("on_sfx_sound_set", self, "on_sfx_sound_set")
	SettingSignal.connect("load_setting_data", self, "on_load_setting_data")
	SettingSignal.connect("left_key", self, "on_left_key_set")
	SettingSignal.connect("right_key", self, "on_right_key_set")
	SettingSignal.connect("up_key", self, "on_up_key_set")
	SettingSignal.connect("down_key", self, "on_down_key_set")
	SettingSignal.connect("skill_1_key", self, "on_skill_1_set")
	SettingSignal.connect("skill_2_key", self, "on_skill_2_set")
	SettingSignal.connect("interact_key", self, "on_interact_set")
