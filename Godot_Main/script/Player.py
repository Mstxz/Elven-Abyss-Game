from godot import exposed, export
from godot import *

@exposed
class Player(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=150.0)
	atk = export(float, default=10.00)
	maxhp = export(float, default=100.0)
	hp = export(float, default=100.0)
	exp = export(int, default=0)
	maxmana = export(float, default=100.0)
	mana = export(float, default=100.0)
	defense = export(float, default=0.0)
	critrate = export(float, default=0.0)
	critdmg = export(float, default=50.0)
	velocity = Vector2()
	
	def _ready(self):
		"""
		Called when the node is added to the scene.
		Initialization happens here.
		"""
		self.sprite = self.get_node("AnimatedSprite")
		pass

	def _process(self, delta):
		"""
		Called every frame. Use it for real-time input handling.
		"""
		self.move(delta)

	def move(self, delta):
		# Get input axis for horizontal movement
		direction_x = Input.get_axis("left", "right")
		direction_y = Input.get_axis("up", "down")
		
		if direction_x or direction_y:
			self.velocity.x = direction_x * self.speed
			self.velocity.y = direction_y * self.speed

			self.sprite.play('Walk') #plays walk animation whenever there is direction input
			if direction_x < 0:
				self.sprite.flip_h = False
				
			elif direction_x > 0:
				self.sprite.flip_h = True
				
		else:
			self.sprite.play('default')  #otherwise plays idle anim
			self.velocity.x = 0
			self.velocity.y = 0  # Stop moving when there's no input
		# Move the KinematicBody2D
		self.velocity = self.move_and_slide(self.velocity)
	
	def hp_changed_func(self):
		#call everytime the health is change (its need to be call to update healthbar)
		healthbar = self.get_node("/root/Node2D/MainUI/ProfileBar/HealthBar")
		healthbar.updatehealth(self.maxhp,self.hp)
	
	def mana_changed_func(self):
		#same as hp just for mana
		manabar = self.get_node("/root/Node2D/MainUI/ProfileBar/ManaBar")
		manabar.updatemana(self.maxmana,self.mana)
	
	def take_damage(self, dmg):
		dmg = min(self.hp,dmg) #max to prevent negative damage turn into healing
		if dmg:
			self.hp -= dmg
			self.hp_changed_func()
		
	def heal(self, amount):
		amount = min(self.maxhp-self.hp,amount) #min to prevent hp over maxhp
		if amount:
			self.hp += amount
			self.hp_changed_func()
			
	def mana_regen(self, amount):
		amount = min(self.maxmana-self.mana,amount) #min to prevent mana over maxmana
		if amount:
			self.mana += amount
			self.mana_changed_func()
	
	def mana_consume(self, amount):
		if amount <= self.mana:
			self.mana -= amount
			self.mana_changed_func()
			return True #might be helpful for checking if have enough mana before using skill
		return False #might be helpful for checking if have enough mana before using skill
		
		
