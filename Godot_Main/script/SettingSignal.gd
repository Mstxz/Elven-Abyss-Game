extends Node

signal on_window_mode_selected(index)

signal on_window_res_selected(index)

signal on_master_sound_set(value)

signal on_music_sound_set(value)

signal on_sfx_sound_set(value)

signal set_setting_dict(setting_dict)

signal load_setting_data(setting_dict)

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
	
