"""Enemy Manager"""
import pygame as game
class Enemy:
    def __init__(self, enemy_hp, enemy_sprite, enemy_dmg, x, y, speed):
        #==========enemy sprite==========#
        self.enemy_sprite = enemy_sprite
        #==========enemy stat==========#
        self.enemy_hp = enemy_hp
        self.enemy_dmg = enemy_dmg
        #==========enemy position==========#
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = self.enemy_sprite.get_rect(topleft=(self.x, self.y))
    
    def move(self, dx, dy):
        """Move the enemy by dx and dy."""
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

    def update(self):
        """Update the enemy's position. You can add more complex movement logic here."""
        self.move(self.speed, 0)
    
    def draw(self, screen):
        """Draw the enemy sprite at the current position."""
        screen.blit(self.enemy_sprite, self.rect.topleft)
