import pygame
import sys
import camera as cam

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
WORLD_WIDTH, WORLD_HEIGHT = 1920 * 2, 1800 * 2

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

# Main game loop
def main():
    clock = pygame.time.Clock()

    player = Player(400, 300)
    camera = cam.Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)
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
        screen.blit(background, (camera.camera.x, camera.camera.y))
        for entity in all_sprites:
            screen.blit(entity.image, camera.apply(entity))

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
