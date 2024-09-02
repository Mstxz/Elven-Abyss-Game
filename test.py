"""Test for smth, nothing interest here"""
import pygame

class Enemy:
    def __init__(self, enemy_hp, enemy_dmg, enemy_sprite, x, y, speed):
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

pygame.init()
screen = pygame.display.set_mode((1920, 1080))

# Load enemy sprite
enemy_sprite = pygame.Surface((50, 50))
enemy_sprite.fill((255, 0, 0))

enemy = Enemy(enemy_hp=100, enemy_dmg=10, enemy_sprite=enemy_sprite, x=500, y=500, speed=0.1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update the enemy
    enemy.update()
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the enemy
    enemy.draw(screen)
    
    # Update the display
    pygame.display.flip()

pygame.quit()
