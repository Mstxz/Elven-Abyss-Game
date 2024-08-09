"""Enemy"""
import main
import player

class Slime:
    def __init__(self):
        #enemy stat
        self.enemy_hp = 20
        self.enemy_dmg = 5

        #enemy movement
        self.enemy_movement_spd = 3