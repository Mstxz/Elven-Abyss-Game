"""Test"""
import pygame as game
import math
import enemy

# Initialize Pygame
game.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
screen = game.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player properties
player_pos = game.Vector2(WIDTH // 2, HEIGHT // 2)
player_speed = 5

# Enemy properties
ENEMY_SIZE = 40
ENEMY_COLOR = RED
ENEMY_SPEED = 2
DETECTION_RADIUS = 300

class Enemy:
    def __init__(self, x, y):
        self.rect = game.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        self.start_x = x
        self.speed = ENEMY_SPEED
        self.direction = 1

    def detect_player(self, player_pos):
        """Detect if the player is within the detection radius."""
        distance_to_player = math.hypot(player_pos.x - self.rect.centerx, player_pos.y - self.rect.centery)
        return distance_to_player < DETECTION_RADIUS

    def chase_player(self, player_pos):
        """Chase the player when detected."""
        if player_pos.x > self.rect.x:
            self.rect.x += self.speed
        elif player_pos.x < self.rect.x:
            self.rect.x -= self.speed

        if player_pos.y > self.rect.y:
            self.rect.y += self.speed
        elif player_pos.y < self.rect.y:
            self.rect.y -= self.speed

    def update(self, player_pos):
        """Update enemy behavior."""
        if self.detect_player(player_pos):
            self.chase_player(player_pos)
        else:
            pass

    def draw(self, surface):
        game.draw.rect(surface, ENEMY_COLOR, self.rect)

# Create an enemy instance
enemy = Enemy(x=100, y=300)
# Game loop
running = True
clock = game.time.Clock()

while running:
    screen.fill((0,0,0))

    # Event handling
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False

    # Player movement (basic WASD controls)
    keys = game.key.get_pressed()
    if keys[game.K_w]:
        player_pos.y -= player_speed
    if keys[game.K_s]:
        player_pos.y += player_speed
    if keys[game.K_a]:
        player_pos.x -= player_speed
    if keys[game.K_d]:
        player_pos.x += player_speed

    # Update enemy
    enemy.update(player_pos)

    # Draw player and enemy
    game.draw.rect(screen, (0, 0, 255), (player_pos.x, player_pos.y, 50, 50))  # Player represented as a blue square
    enemy.draw(screen)

    # Update the display
    game.display.flip()
    clock.tick(120)

# Quit Pygame
game.quit()
