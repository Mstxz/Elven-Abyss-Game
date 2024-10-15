from godot import exposed, export
from godot import *

elemdict = {
	'Water' : 0,
	'Fire' : 1,
	'Wind' : 2,
	'Earth' : 3
}
		
weapondict = {
	'Stick' : 0,
	'Spellbook' : 1,
	'Staff' : 2,
	'Bow' : 3,
	'Crossbow' : 4,
	'Gun' : 5
}


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
	weapon = export(str, default='Staff')
	element = export(str, default="Water")
	velocity = Vector2()
	
	
	def _ready(self):
		"""
		Called when the node is added to the scene.
		Initialization happens here.
		"""
		self.sprite = self.get_node('AnimatedSprite')
		
		#prepare animation id (str() is require twice to convert gdstring to string)
		self.animationid = str(elemdict[str(self.element)]) + str(weapondict[str(self.weapon)])
		
		self.wait(5,'testwait')
	
	def _process(self, delta):
		"""
		Called every frame. Use it for real-time input handling.
		"""
		self.move(delta)
		
	def wait(self,time,funcname):
		self.timer = Timer.new()
		self.timer.wait_time = time
		self.timer.one_shot = True
		self.add_child(self.timer)
		
		# Connect the timeout signal to a custom method
		self.timer.connect("timeout", self, funcname)
		
		# Start the timer
		self.timer.start()
	
	def testwait(self):
		print('delay has timed out')



	def move(self, delta):
		"""Movement System"""
		direction_x = Input.get_axis("left", "right")
		direction_y = Input.get_axis("up", "down")
		
		if direction_x or direction_y:
			#-+-+-+-+-Player Moving-+-+-+-+-#
			self.velocity.x = direction_x * self.speed
			self.velocity.y = direction_y * self.speed
			
			self.sprite.play('Walk' + self.animationid) #Player Animation
			if direction_x < 0:
				self.sprite.flip_h = False

			elif direction_x > 0:
				self.sprite.flip_h = True
			
			#elif direction_y > 0:
				#self.sprite.play("run_d")
			#elif direction_y < 0:
				#self.sprite.play("run_u")
				
		else:
			self.sprite.play('Idle' + self.animationid)
			
			self.velocity.x = 0
			self.velocity.y = 0  # Stop moving when there's no input
		self.velocity = self.move_and_slide(self.velocity)
		
	
	def hp_changed_func(self):
		
		healthbar = self.get_node("/root/Node2D/MainUI/ProfileBar/HealthBar")
		healthbar.updatehealth(self.maxhp,self.hp)
	
	def mana_changed_func(self):
		#same as hp just for mana
		manabar = self.get_node("/root/Node2D/MainUI/ProfileBar/ManaBar")
		manabar.updatemana(self.maxmana,self.mana)
	
	def take_damage(self, dmg):
		dmg = max(dmg-self.defense, 1) #reduce damage with defense with the least possible dmg is 1
		dmg = min(self.hp,dmg)
		if dmg:
			self.hp -= dmg
			self.hp_changed_func()
		
	def heal(self, amount):
		amount = min(self.maxhp-self.hp,amount)
		if amount:
			self.hp += amount
			self.hp_changed_func()
			
	def mana_regen(self, amount):
		amount = min(self.maxmana-self.mana,amount)
		if amount:
			self.mana += amount
			self.mana_changed_func()
	
	def mana_consume(self, amount):
		if amount <= self.mana:
			self.mana -= amount
			self.mana_changed_func()
			return True
		return False
		
		
