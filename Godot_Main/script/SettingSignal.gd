extends Node

signal on_window_mode_selected(index)

signal on_window_res_selected(index)

signal on_master_sound_set(value)

signal on_music_sound_set(value)

signal on_sfx_sound_set(value)

signal set_setting_dict(setting_dict)

signal load_setting_data(setting_dict)

signal left_key(array)

signal right_key(array)

signal up_key(array)

signal down_key(array)

signal skill_1_key(array)

signal skill_2_key(array)

signal interact_key(array)

func load_setting(setting_dict: Dictionary):
	#update value to signal
	emit_signal("load_setting_data", setting_dict)

func select_window_mode(index: int):
	#update value to signal
	emit_signal("on_window_mode_selected", index)

func select_window_res(index: int):
	#update value to signal
	emit_signal("on_window_res_selected", index)

func set_master_sound(value: float):
	#update value to signal
	emit_signal("on_master_sound_set", value)

func set_music_sound(value: float):
	#update value to signal
	emit_signal("on_music_sound_set", value)

func set_sfx_sound(value: float):
	#update value to signal
	emit_signal("on_sfx_sound_set", value)

func update_settings(setting_dict: Dictionary):
	#update value to signal
	emit_signal("set_setting_dict", setting_dict)

func set_left_key(array: int):
	emit_signal("left_key", array)

func set_right_key(array: int):
	emit_signal("right_key", array)

func set_up_key(array: int):
	emit_signal("up_key", array)

func set_down_key(array: int):
	emit_signal("down_key", array)

func set_skill_1_key(array: int):
	emit_signal("skill_1_key", array)

func set_skill_2_key(array: int):
	emit_signal("skill_2_key", array)

func set_interact_key(array: int):
	emit_signal("interact_key", array)
