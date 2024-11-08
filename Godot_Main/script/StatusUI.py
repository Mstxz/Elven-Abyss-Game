from godot import exposed, export
from godot import *


@exposed
class StatusUI(CanvasLayer):

	def _ready(self):
		self.level = self.get_node("Panel/InfoContainer/HBoxContainer/VBoxContainer2/Label6")
		self.exp = self.get_node("Panel/InfoContainer/HBoxContainer/VBoxContainer2/Label5")
		self.element = self.get_node("Panel/InfoContainer/HBoxContainer/VBoxContainer2/Label2")
		self.weapon = self.get_node("Panel/InfoContainer/HBoxContainer/VBoxContainer2/Label3")
		self.money = self.get_node("Panel/InfoContainer/HBoxContainer/VBoxContainer2/Label4")
		self.hp = self.get_node("Panel/StatContainer/StatValue/HP")
		self.atk = self.get_node("Panel/StatContainer/StatValue/ATK")
		self.defense = self.get_node("Panel/StatContainer/StatValue/DEF")
		self.spd = self.get_node("Panel/StatContainer/StatValue/SPD")
		self.crirate = self.get_node("Panel/StatContainer/StatValue/CRTR")
		self.cridam = self.get_node("Panel/StatContainer/StatValue/CRTD")
		self.mana = self.get_node("Panel/StatContainer/StatValue/MANA")
		self.skillpoint = self.get_node("Panel/StatsPoint")
		self.player = self.get_node("../Player")

	def setvar(self):
		self.level.text = str(f"{int(self.player.level)}")
		self.exp.text = str(f"{int(self.player.exp)}")
		self.element.text = str(self.player.element)
		self.weapon.text = str(self.player.weapon)
		self.money.text = str(int(self.player.money))
		self.hp.text = str(f"{self.player.hp:.1f}/{self.player.maxhp}")
		self.atk.text = str(int(self.player.atk))
		self.defense.text = str(int(self.player.defense))
		self.spd.text = str(int(self.player.speed))
		self.crirate.text = str(int(self.player.critrate))
		self.cridam.text = str(int(self.player.critdmg))
		self.mana.text = str(f"{self.player.mana:.1f}/{self.player.maxmana}")
		self.skillpoint.text = str(f"Stats Point : {self.player.skillpoint} Point")

	def _on_HPbutton_pressed(self):
		if self.player.skillpoint > 0:
			self.player.skillpoint -= 1
			self.player.maxhp += 10
			self.player.hp += 10
			self.setvar()
			self.player.updatevar()

	def _on_ATKbutton_pressed(self):
		if self.player.skillpoint > 0:
			self.player.skillpoint -= 1
			self.player.atk += 2
			self.setvar()
			self.player.updatevar()

	def _on_DEFbutton_pressed(self):
		if self.player.skillpoint > 0:
			self.player.skillpoint -= 1
			self.player.defense += 2
			self.setvar()
			self.player.updatevar()

	def _on_SPDbutton_pressed(self):
		if self.player.skillpoint > 0:
			self.player.skillpoint -= 1
			self.player.speed += 10
			self.setvar()
			self.player.updatevar()

	def _on_CRITRbutton_pressed(self):
		if self.player.skillpoint > 0:
			self.player.skillpoint -= 1
			self.player.critrate += 5
			self.setvar()
			self.player.updatevar()

	def _on_CRITDbutton_pressed(self):
		if self.player.skillpoint > 0:
			self.player.skillpoint -= 1
			self.player.critdmg += 5
			self.setvar()
			self.player.updatevar()

	def _on_MANAbutton_pressed(self):
		if self.player.skillpoint > 0:
			self.player.skillpoint -= 1
			self.player.mana += 10
			self.player.maxmana += 10
			self.setvar()
			self.player.updatevar()
