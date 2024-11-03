extends Control

export(String) var action_name = ""
var label: Label
var button: Button
var key_name: String = ""

func _ready():
	initialize_nodes()
	set_process_unhandled_key_input(false)
	set_action_name()
	set_text_for_key()

func initialize_nodes():
	# Attempt to get nodes and handle potential errors
	label = $HBoxContainer/Label
	button = $HBoxContainer/Button

func set_action_name():
	if action_name in ["up", "down", "left", "right"]:
		label.text = "Move " + action_name.capitalize()
	else:
		label.text = action_name.capitalize()

func set_text_for_key():
	var action_events = InputMap.get_action_list(action_name)
	if action_events.size() > 0:
		# Find the first key event
		for event in action_events:
			if event is InputEventKey:
				var key_code = event.scancode
				key_name = OS.get_scancode_string(key_code)
				button.text = key_name
				return

func update_button_text():
	if key_name:
		button.text = key_name
	else:
		button.text = "No key bound"

func _on_Button_toggled(button_press: bool):
	if button_press:
		button.text = "Press any key"
		set_process_unhandled_key_input(true)  # Enable key input processing
	else:
		update_button_text()  # Update button text on toggle off
		set_process_unhandled_key_input(false)  # Disable key input processing
		button.pressed = false  # Explicitly toggle the button off

func _unhandled_key_input(event):
	if event is InputEventKey and event.pressed:
		# Check if the key is already bound to the action
		var current_events = InputMap.get_action_list(action_name)

		for evt in current_events:
			if evt.scancode == event.scancode:
				print("Key ", OS.get_scancode_string(event.scancode), " is already bound.")
				return  # Exit early if the key is already bound

		# Clear current events associated with the action
		InputMap.action_erase_events(action_name)

		# Create a new key event and add it to the action
		var new_event = InputEventKey.new()
		new_event.scancode = event.scancode
		InputMap.action_add_event(action_name, new_event)

		# Update the button text to reflect the new key binding
		key_name = OS.get_scancode_string(event.scancode)
		button.text = key_name

		# Disable key input processing and turn the button off
		set_process_unhandled_key_input(false)
		_on_Button_toggled(false)  # Ensure button state is off

func _exit_tree():
	set_process_unhandled_key_input(false)

	# Clear node references
	label = null
	button = null
	key_name = ""

func _notification(what):
	if what == NOTIFICATION_EXIT_TREE:
		_exit_tree()
