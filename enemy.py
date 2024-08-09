import pygame
import main

class Enemy:
    def __init__(self):
        self.image = pygame.image.load("Assets/Sprite/36px-Red_Sludge.png")
        self.health = 100  # Example health attribute
        self.speed = 2  # Example speed attribute

    def move_towards_player(self, player_pos):
        """Move the enemy towards the player's position."""
        dx, dy = player_pos[0] - self.image.get_width(), player_pos[1] - self.image.get_height()
        distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
        dx, dy = dx / distance, dy / distance  # Normalize the direction vector

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def update(self, player_pos):
        """Update the enemy's position."""
        self.move_towards_player(player_pos)

    def draw(self, screen):
        """Draw the enemy on the screen."""
        screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        """Check if the enemy collides with the player."""
        if self.rect.colliderect(player_rect):
            print("Enemy hit the player!")
