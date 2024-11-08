from godot import *
import random

#Load Scene here
projectile = ResourceLoader.load("res://scene/EnergyBall.tscn")
arrow = ResourceLoader.load("res://scene/Arrow.tscn")
bubble = ResourceLoader.load("res://scene/Bubble.tscn")
gameover = ResourceLoader.load("res://scene/GameOver.tscn")

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

elemcolordict = {
	'Water' : Color(0,0.45,1,0.8),
	'Fire' : Color(1,0.5,0,0.8),
	'Wind' : Color(0,0.76,0.6,0.8),
	'Earth' : Color(0.75,0.54,0,0.8)
}

@exposed
class Player(KinematicBody2D):

	# member variables here, example:
	speed = export(float, default=150.0)
	atk = export(float, default=10.00)
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
	acting = export(bool, default=False)
	skill1cd = export(bool, default=False)
	skill2cd = export(bool, default=False)
	invincible = export(bool, default=False)
	freeze = export(bool, default=False)
	
	enemybubbled = []
	skill0activate = False
	velocity = Vector2()
	knockbacked = Vector2() #set in take_damage and reduce by a rate in each _progress
	mousepos = Vector2()
	
	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.PlayerVar = self.get_tree().get_root().get_node("/root/PlayerVar")
		
		self.getvar()
		#prepare animation id (str() is require twice to convert gdstring to string)
		self.updateplayer()
		
		#locate for later uses
		self.main = self.get_parent()
		self.sprite = self.get_node('AnimatedSprite')
		self.uicd1 = self.get_parent().get_node("MainUI/Skill1Cd")
		self.uicd2 = self.get_parent().get_node("MainUI/Skill2Cd")
		self.moneyui = self.get_parent().get_node("MainUI/ProfileBar/Money")
		self.levelui = self.get_parent().get_node("MainUI/ProfileBar/Level")
		self.animplayer = self.get_node('AnimationPlayer')
		
		#update ui
		self.moneyui.updateui(self.money)
		self.levelui.updateui(self.level)
		self.hp_changed_func()
		self.mana_changed_func()
		
	def _process(self, delta):
		"""Called every rendering process"""
		self.mana_regen(delta*4)
		if self.main.pause or self.freeze or self.hp <= 0:
			return
		self.move(delta+self.maxmana//1000)
		if not self.acting and not self.get_tree().is_input_handled():
			self.shoot()
			self.skill1()
			self.skill2()
	
	def wait(self,time,funcname,para=Array()):
		'''connect to a function after delays'''
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
	
	def cooldown(self,target=None,timeout=False):
		'''frequently use to reset cooldown after the timer'''
		if self.sprite.is_connected("animation_finished",self,"cooldown") and not target:
			self.sprite.disconnect("animation_finished",self,"cooldown")
			if not timeout and not target:
				return
		if not target:
			self.acting = False
		else:
			target = str(target)
		if target == 'skill1':
			self.skill1cd = False
		elif target == 'skill2':
			self.skill2cd = False
	
	def updateplayer(self):
		'''reset animation when chaning weapon or element'''
		#prepare animation id (str() is require twice to convert gdstring to string)
		self.animationid = str(elemdict[str(self.element)]) + str(weapondict[str(self.weapon)])
		profileui = self.get_node("../MainUI/Viewport/AnimatedSprite")
		
		profileui.play('Idle'+self.animationid)
		self.sprite = self.get_node('AnimatedSprite')
		self.sprite.play('Idle'+self.animationid)
	
	def shoot(self,part=0):
		'''player shoots projectile toward cursor'''
		if str(self.weapon) == 'Stick':
			if not part and Input.is_action_just_pressed('left_click') and not self.acting:
				# if the player click
				if self.mana_consume(5):
					#acting is as it name suggest to prevent spam
					self.acting = True
					self.sprite.play('Shoot' + self.animationid)
					self.mousepos = self.get_global_mouse_position()#get mouse pos
					if self.mousepos.x > self.position.x:
						self.sprite.flip_h = True
					else:
						self.sprite.flip_h = False
					self.wait(0.3,'shoot',[part+1])
			elif part == 1:
				# 'projectile' is loaded scene sees at the start of this script
				bullet = projectile.instance()
				#get direction from mousepos turn it into proper angle value
				direction = (self.position - self.mousepos).angle()
				#set projectile property
				bullet.direction = direction
				bullet.spawnpos = self.position + (self.position - self.mousepos) * -0.22
				bullet.spawnrot = direction
				random1 = random.uniform(0.1, 100.0)
				if random1 <= self.critrate:
					bullet.damage = self.atk + (self.atk * (self.critdmg / 100))
				else:
					bullet.damage = self.atk
				bullet.speed = 50
				bullet.duration = 6
				#add it
				self.main.add_child(bullet)
				#set self.acting back to False after the set time
				self.wait(0.25,'cooldown',[None,True])
				self.sprite.connect("animation_finished",self,"cooldown")
		elif str(self.weapon) == 'Staff':
			if not part and Input.is_action_just_pressed('left_click'):
				# if the player click
				if not self.acting:
					if self.mana_consume(10):
						#acting is as it name suggest to prevent spam and
						#keep the animation running
						self.acting = True
						self.sprite.play('Shoot' + self.animationid)
						self.mousepos = self.get_global_mouse_position()#get mouse pos
						if self.mousepos.x > self.position.x:
							self.sprite.flip_h = True
						else:
							self.sprite.flip_h = False
						self.wait(0.3,'shoot',[part+1])
			elif part == 1:
				# 'projectile' is loaded scene sees at the start of this script
				bulletoffset = [
					Vector2(0,-50),
					Vector2(35,-20),
					Vector2(-35,-20),
					Vector2(25,30),
					Vector2(-25,30)
				]
				for i in range(5):
					bullet = projectile.instance()
					#get direction from mousepos turn it into proper angle value
					direction = ((self.position + bulletoffset[i]) - self.mousepos).angle()
					#set projectile property
					bullet.direction = direction
					bullet.spawnpos = self.position + bulletoffset[i]
					bullet.spawnrot = direction
					bullet.speed = 150
					bullet.duration = 6
					bullet.damage = self.atk*0.9
					bullet.spin_speed = 20
					bullet.knockback = 10
					bullet.modulate = elemcolordict[str(self.element)]
					bullet.get_node("Light2D").color = elemcolordict[str(self.element)]
					#add it
					self.main.add_child(bullet)
				#set self.acting back to False after the set time
				self.wait(0.35,'cooldown',[None,True])
				self.sprite.connect("animation_finished",self,"cooldown")
		elif str(self.weapon) == 'Crossbow':
			if not part and Input.is_action_just_pressed('left_click') and not self.acting:
				# if the player click
				#acting is as it name suggest to prevent spam
				self.acting = True
				self.sprite.play('Shoot' + self.animationid)
				self.mousepos = self.get_global_mouse_position()#get mouse pos
				if self.mousepos.x > self.position.x:
					self.sprite.flip_h = True
				else:
					self.sprite.flip_h = False
				bullet = arrow.instance()
				#get direction from mousepos turn it into proper angle value
				direction = (self.position - self.mousepos).angle()
				#set projectile property
				bullet.direction = direction
				bullet.spawnpos = self.position + (self.position - self.mousepos) * -0.22
				bullet.spawnrot = direction
				bullet.damage = self.atk
				bullet.target = 'Enemy'
				bullet.duration = 6
				#add it
				self.main.add_child(bullet)
				#set self.acting back to False after the set time
				self.wait(0.25,'cooldown',[None,True])
				self.sprite.connect("animation_finished",self,"cooldown")
		
	def move(self, delta):
		"""Movement System"""
		direction_x = Input.get_axis("left", "right")
		direction_y = Input.get_axis("up", "down")
		currentanim = str(self.sprite.animation)
		if abs(self.knockbacked.x) + abs(self.knockbacked.y) > 5:
			# in case theres no player in range and theres still kb
			# so this have to be outside main if
			self.velocity *= 0.9
			self.knockbacked *= 0.9
			self.move_and_slide(self.velocity)
		elif (direction_x or direction_y) and not self.freeze:
			#-+-+-+-+-Player Moving-+-+-+-+-#
			self.velocity.x = direction_x * self.speed
			self.velocity.y = direction_y * self.speed
			animation = ''
			
			def flip():
				if direction_x < 0:
					self.sprite.flip_h = False
				elif direction_x > 0:
					self.sprite.flip_h = True
				
			if not self.acting:
				flip()
				animation = 'Walk' + self.animationid
			elif 'Shoot' in currentanim and not 'Walk' in currentanim:
				frame = self.sprite.frame
				animation = 'ShootWalk'+ self.animationid
				self.sprite.play(animation)
				self.sprite.frame = frame
			elif self.skill0activate:
				animation = 'Skill0Walk'
				sfx = self.get_node('Sfx').get_node('Skill1Water_Walk')
				if sfx.playing == False:
					sfx.play()
				flip()
			if animation:
				self.sprite.play(animation)
		else:
			animation = ''
			if not self.acting:
				animation = 'Idle' + self.animationid
			elif self.skill0activate:
				animation = 'Skill0Idle'
				self.stopsfx('Skill1Water_Walk')
			elif 'Shoot' in currentanim and 'Walk' in currentanim:
				frame = self.sprite.frame
				animation = 'Shoot'+ self.animationid
				self.sprite.play(animation) #play early to reset frame
				self.sprite.frame = frame
			if animation:
				self.sprite.play(animation)
			self.velocity.x = 0
			self.velocity.y = 0  # Stop moving when there's no input
		self.velocity = self.move_and_slide(self.velocity)
	
	def playsfx(self,sfxname):
		sfx = self.get_node('Sfx').get_node(sfxname)
		sfx.play()
	
	def stopsfx(self,sfxname):
		sfx = self.get_node('Sfx').get_node(sfxname)
		sfx.stop()
	
	def skill1(self,part=0):
		if str(self.element) == 'Water':
			cdtime = 10
			if not self.skill1cd and Input.is_action_just_pressed('skill1') and not part:
				if self.mana_consume(20):
					self.freeze = True
					self.skill1cd = True
					self.acting = True
					self.invincible = True
					self.wait(0.5,'playsfx',['Skill1Water_Enter'])
					self.sprite.play('Skill'+ self.animationid)
					self.sprite.connect("animation_finished",self,"skill1",Array([part+1]))
					self.uicd1.activating(self.element)
			elif part == 1:
				self.sprite.disconnect("animation_finished",self,"skill1")
				self.freeze = False
				self.skill0activate = True
				self.invincible = True
				self.sprite.play('Skill0Idle')
				self.wait(5,'skill1',[part+1])
			elif part == 2:
				self.freeze = True
				self.skill0activate = False
				self.invincible = True
				self.sprite.play('Skill'+ self.animationid + 'Cancel')
				self.sprite.connect("animation_finished",self,"skill1",Array([part+1]))
			elif part == 3:
				self.playsfx('Skill1Water_Exit')
				self.stopsfx('Skill1Water_Walk')
				self.sprite.disconnect("animation_finished",self,"skill1")
				self.invincible = False
				self.acting = False
				self.freeze = False
				self.wait(cdtime,'cooldown',['skill1'])
				self.uicd1.cooldownui(cdtime) #call ui func
	
	def skill2(self,part=0,param1=None):
		if str(self.element) == 'Water':
			if not self.skill2cd and Input.is_action_just_pressed('skill2') and not part:
				if self.mana_consume(80):
					self.skill2cd = True
					self.freeze = True
					self.sprite.play('Ult'+ self.animationid)
					self.sprite.connect('animation_finished',self,'updateplayer')
					self.wait(1,'skill2',[part+1])
			elif part == 1:
				self.animplayer.play('WaterSkill2')
				allbodies = self.get_node("WaterSkill2Area").get_overlapping_bodies()
				for i in allbodies:
					if 'Enemy' in str(i.name): #prevent recognizing other kinematic2d
						if i.died:
							return
						i.freeze = True
						i.get_node('AnimatedSprite').play('Idle')
						givebubble = bubble.instance()
						givebubble.scale += i.scale
						if 'Boss' in str(i.name):
							givebubble.scale += Vector2(2,2)
						i.add_child(givebubble)
						i.wait(10,'bubblepop')
				self.wait(1.2,'skill2',[part+1])
			elif part == 2:
				cdtime = 20
				self.freeze = False
				self.sprite.disconnect('animation_finished',self,'updateplayer')
				self.wait(cdtime,'cooldown',['skill2'])
				self.uicd2.cooldownui(cdtime) #call ui func
	
	def hp_changed_func(self):
		
		healthbar = self.get_node("../MainUI/ProfileBar/HealthBar")
		healthbar.updatehealth(self.maxhp,self.hp)
	
	def mana_changed_func(self):
		#same as hp just for mana
		manabar = self.get_node("../MainUI/ProfileBar/ManaBar")
		manabar.updatemana(self.maxmana,self.mana)
	
	def take_damage(self, dmg, kb=None):
		'''handle taking damage'''
		if self.invincible or self.hp <= 0:
			return
		#reduce damage with defense with the least possible dmg is 1
		dmg = max(dmg-self.defense, 1)
		dmg = min(dmg,self.hp)
		if kb: #kb stands for knockback
			self.velocity = kb
			self.knockbacked = kb
			self.move_and_slide(self.velocity)
		if dmg: #handle dmg
			self.hp -= dmg
			self.hp_changed_func()
		if self.hp <= 0:
			self.death()
	
	def death(self):
		'''handle player when die'''
		self.freeze = True
		overui = gameover.instance()
		self.main.add_child(overui)
		self.sprite.play('Died')
		overui.get_node("AnimationPlayer").play('GameOver')
		self.playsfx('GameOverSfx')
		
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
		
	def money_modify(self,amount):
		if self.money + amount < 0 :
			return False
		self.money += amount
		self.moneyui.updateui(self.money)
		return True
		
			
	def gain_exp(self,amount):
		'''call when giving exp to player'''
		self.exp += amount*2
	
	def changeweapon(self,weapon):
		'''change weapon to ...'''
		self.weapon = weapon
		self.updateplayer()

	def changeelement(self,element):
		'''change element to ...'''
		self.element = element
		self.updateplayer()
	
	def updatevar(self):
		'''update player var to global'''
		self.PlayerVar.speed = self.speed
		self.PlayerVar.atk = self.atk
		self.PlayerVar.maxhp = self.maxhp
		self.PlayerVar.hp = self.hp
		self.PlayerVar.level = self.level
		self.PlayerVar.exp = self.exp
		self.PlayerVar.money = self.money
		self.PlayerVar.maxmana = self.maxmana
		self.PlayerVar.mana = self.mana
		self.PlayerVar.defense = self.defense
		self.PlayerVar.critrate = self.critrate
		self.PlayerVar.critdmg = self.critdmg
		self.PlayerVar.weapon = self.weapon
		self.PlayerVar.element = self.element
		self.PlayerVar.skillpoint = self.skillpoint
		
	def getvar(self):
		'''get player var from global'''
		self.speed = self.PlayerVar.speed
		self.atk = self.PlayerVar.atk
		self.maxhp = self.PlayerVar.maxhp
		self.hp = self.PlayerVar.hp
		self.level = self.PlayerVar.level
		self.exp = self.PlayerVar.exp
		self.money = self.PlayerVar.money
		self.maxmana = self.PlayerVar.maxmana
		self.mana = self.PlayerVar.mana
		self.defense = self.PlayerVar.defense
		self.critrate = self.PlayerVar.critrate
		self.critdmg = self.PlayerVar.critdmg
		self.weapon = self.PlayerVar.weapon
		self.element = self.PlayerVar.element
		self.skillpoint = self.PlayerVar.skillpoint
