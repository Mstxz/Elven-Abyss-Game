import pygame
import sys

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set room dimensions
ROOM_WIDTH, ROOM_HEIGHT = 1200, 800

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player setup
player_size = 50
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT // 2 - player_size // 2
player_speed = 5

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle key presses for movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    
    # Enforce room boundaries
    if player_x < (SCREEN_WIDTH - ROOM_WIDTH) // 2:
        player_x = (SCREEN_WIDTH - ROOM_WIDTH) // 2
    if player_x + player_size > (SCREEN_WIDTH + ROOM_WIDTH) // 2:
        player_x = (SCREEN_WIDTH + ROOM_WIDTH) // 2 - player_size
    if player_y < (SCREEN_HEIGHT - ROOM_HEIGHT) // 2:
        player_y = (SCREEN_HEIGHT - ROOM_HEIGHT) // 2
    if player_y + player_size > (SCREEN_HEIGHT + ROOM_HEIGHT) // 2:
        player_y = (SCREEN_HEIGHT + ROOM_HEIGHT) // 2 - player_size

    # Draw everything
    screen.fill(WHITE)
    
    # Draw room boundary (optional)
    pygame.draw.rect(screen, RED, [(SCREEN_WIDTH - ROOM_WIDTH) // 2, 
                                   (SCREEN_HEIGHT - ROOM_HEIGHT) // 2, 
                                   ROOM_WIDTH, ROOM_HEIGHT], 2)
    
    # Draw player
    pygame.draw.rect(screen, RED, [player_x, player_y, player_size, player_size])
    
    # Update display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(120)

# Clean up
pygame.quit()
sys.exit()
