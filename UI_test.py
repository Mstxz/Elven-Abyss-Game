import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump System")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Player settings
player_width = 50
player_height = 50

#player spawn position
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height

player_velocity_y = 0
gravity = 1
jump_strength = -20
on_ground = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()
    
    # Jump when space is pressed and player is on the ground
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_strength
        on_ground = False

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Collision with the ground
    if player_y >= SCREEN_HEIGHT - player_height:
        player_y = SCREEN_HEIGHT - player_height
        player_velocity_y = 0
        on_ground = True

    # Clear screen
    screen.fill(WHITE)

    # Draw player
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
