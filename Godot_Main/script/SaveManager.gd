extends Node

const SETTING_SAVE_PATH: String = "user://SettingData.save"
var setting_data_dict: Dictionary = {}

func _ready():
	SettingSignal.connect("set_setting_dict", self, "on_setting_save")
	load_setting()

func on_setting_save(data: Dictionary) -> void:
	setting_data_dict = data  # Store the incoming settings data

	# Serialize the dictionary to JSON
	var json_data = to_json(setting_data_dict)
	
	#  JSON data to string
	var encrypted_data = String(json_data)

	# Create a new File instance
	var file = File.new()
	var error = file.open(SETTING_SAVE_PATH, File.WRITE)
	if error == OK:
		file.store_string(encrypted_data)  # Write the encrypted data
		file.close()  # Close the file

func load_setting() -> void:

	# Create a new File instance
	var file = File.new()
	var checked = file.open(SETTING_SAVE_PATH, File.READ)
	if checked == OK:
		# Read the encrypted data
		var encrypted_data = file.get_as_text()
		file.close()  # Close the file


		# Decrypt the data
		var json_data = JSON.parse(encrypted_data).result
		SettingSignal.load_setting(Dictionary(json_data))
