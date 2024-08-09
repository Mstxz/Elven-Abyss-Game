import pygame

class Enemy:
    def __init__(self, x, y, width, height, color, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        self.health = 100

    def move_towards_player(self, player_pos):
        # Simple logic to move towards the player
        if self.rect.x < player_pos[0]:
            self.rect.x += self.speed
        elif self.rect.x > player_pos[0]:
            self.rect.x -= self.speed

        if self.rect.y < player_pos[1]:
            self.rect.y += self.speed
        elif self.rect.y > player_pos[1]:
            self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            # Enemy is defeated, you can add more logic here



# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Player position for enemy to chase
player_pos = [400, 300]

# Create an enemy instance
enemy = Enemy(x=100, y=100, width=50, height=50, color=(255, 0, 0), speed=2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Enemy movement towards player
    enemy.move_towards_player(player_pos)

    # Update display
    screen.fill((0, 0, 0))  # Clear the screen
    enemy.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
