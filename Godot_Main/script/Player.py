from godot import *

#Load Scene here
projectile = ResourceLoader.load("res://scene/EnergyBall.tscn")

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
	acting = export(bool, default=False)
	velocity = Vector2()
	
	def _ready(self):
		
		#prepare animation id (str() is require twice to convert gdstring to string)
		self.animationid = str(elemdict[str(self.element)]) + str(weapondict[str(self.weapon)])
		profileui = self.get_node("/root/Node2D/MainUI/Viewport/AnimatedSprite")
		profileui.play('Idle'+self.animationid)
		
		#locate for later uses
		self.main = self.get_node("/root/Node2D")
		self.sprite = self.get_node('AnimatedSprite')
		
	def _process(self, delta):
		if not self.acting:
			self.move(delta)
			if self.get_tree().is_input_handled():
				#return if the input is handled by ui
				return
			self.shoot()
		
	
	def wait(self,time,funcname,para=Array()):
		'''see example in shoot()'''
		timer = Timer.new()
		timer.one_shot = True
		self.add_child(timer)
		
		# Connect the timeout signal to a custom method
		timer.connect("timeout", self, funcname, Array(para))
		timer.connect("timeout", self, 'cleartimer', Array([timer]))
		# Start the timer
		timer.start(time)
	
	def cleartimer(self,timer):
		'''sole purpose to delete timer made from wait()'''
		timer.queue_free()
	
	def cooldown(self):
		'''frequently use to let the player act after the timer'''
		self.acting = False
	
	def shoot(self,mousepos=0,part=0):
		'''player shoots projectile toward cursor'''
		if not part:
			if Input.is_action_just_pressed('left_click'):
				# if the player click
				if not self.acting:
					#acting is as it name suggest to prevent spam and
					#keep the animation running
					self.acting = True
					mousepos = self.get_global_mouse_position()
					self.sprite.play('Shoot' + self.animationid)
					if mousepos.x > self.position.x:
						self.sprite.flip_h = True
					else:
						self.sprite.flip_h = False
					self.wait(0.3,'shoot',[mousepos,part+1])
		elif part == 1:
			# 'projectile' is loaded scene sees at the start of this script
			bullet = projectile.instance()
			#get direction from mousepos turn it into proper angle value
			direction = (self.position - mousepos).angle()
			#set projectile property
			bullet.direction = direction
			bullet.spawnpos = self.position + (self.position - mousepos) * -0.22
			bullet.spawnrot = direction
			bullet.speed = 50
			bullet.duration = 6
			#add it
			self.main.add_child(bullet)
			
			#set self.acting back to False after the set time
			self.wait(0.35,'cooldown')
		
	def move(self, delta):
		"""Movement System"""
		direction_x = Input.get_axis("left", "right")
		direction_y = Input.get_axis("up", "down")
		
		if (direction_x or direction_y):
			#-+-+-+-+-Player Moving-+-+-+-+-#
			self.velocity.x = direction_x * self.speed
			self.velocity.y = direction_y * self.speed
			
			self.sprite.play('Walk' + self.animationid) #Player Animation
			if direction_x < 0:
				self.sprite.flip_h = False

			elif direction_x > 0:
				self.sprite.flip_h = True
			
				
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
		
		
