import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WORLD_WIDTH, WORLD_HEIGHT = 1600, 1200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Camera Example")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [
            pygame.image.load("Assets/Sprite/Player_Anabelle.png"),  
            pygame.image.load("Assets/Sprite/Player_Anabelle_Left.png"), 
            pygame.image.load("Assets/Sprite/Player_Anabelle_Right.png"),
            pygame.image.load("Assets/Sprite/Player_Anabelle_Back.png")
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = 'down'
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = self.images[1]
            self.direction = 'left'
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.images[2]
            self.direction = 'right'
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.image = self.images[3]
            self.direction = 'up'
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.image = self.images[0]
            self.direction = 'down'

class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.world_width - self.width), x)  # right
        y = max(-(self.world_height - self.height), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Main game loop
def main():
    clock = pygame.time.Clock()

    player = Player(400, 300)
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)
    background = pygame.image.load("Assets/Sprite/BG.jpg")
    background = pygame.transform.scale(background, (WORLD_WIDTH, WORLD_HEIGHT))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player and camera
        all_sprites.update()
        camera.update(player)

        # Draw everything
        screen.fill((0, 0, 0))
        screen.blit(background, camera.apply(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT)))
        for entity in all_sprites:
            screen.blit(entity.image, camera.apply(entity))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
