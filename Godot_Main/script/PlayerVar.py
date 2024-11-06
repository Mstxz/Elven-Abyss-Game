from godot import exposed, export
from godot import *


@exposed
class PlayerVar(Node):

	# member variables here, example:
	speed = export(float, default=150.0)
	atk = export(float, default=10.0)
	maxhp = export(float, default=100.0)
	hp = export(float, default=100.0)
	level = export(int, default=1)
	exp = export(float, default=0.0)
	money = export(int, default=100)
	maxmana = export(float, default=100.0)
	mana = export(float, default=100.0)
	defense = export(float, default=0.0)
	critrate = export(float, default=0.0)
	critdmg = export(float, default=50.0)
	weapon = export(str, default='Stick')
	element = export(str, default="Water")
	skillpoint = export(int, default=0)

