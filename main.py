"""main game"""
import pygame as game
import pygame.camera
class Gui:
    """Gui and Screen"""
    def __init__(self):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1920, 1080
        self.screen = game.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        game.display.set_caption("Elven Abyss")
        icon_image = game.image.load("Assets/Sprite/Sebastian_Icon.png")
        game.display.set_icon(icon_image)
        background = game.image.load("Assets/Sprite/BG.jpg")
        self.background = game.transform.scale(background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw(self, player):
        """Draw everything"""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(player.player_img, player.player_pos)
        game.display.update()

class Player:
    """Player class"""
    def __init__(self, player_images):
        self.player_imgs = player_images
        self.player_img = self.player_imgs[0]
        self.player_pos = [960, 540]
        self.movement = [0, 0]

    def handle_event(self, event, speed):
        """Handle player input"""
        if event.type == game.KEYDOWN:
            match event.key:
                case game.K_a:
                    self.movement[0] = -speed
                    self.player_img = self.player_imgs[1]
                case game.K_d:
                    self.movement[0] = speed
                    self.player_img = self.player_imgs[2]
        elif event.type == game.KEYUP:
            if event.key in (game.K_a, game.K_d):
                self.movement[0] = 0
                self.player_img = self.player_imgs[0]

    def update_position(self, screen_width, screen_height):
        """Update player position"""
        self.player_pos[0] = max(0, min(self.player_pos[0] + self.movement[0], screen_width - self.player_img.get_width()))
        self.player_pos[1] = max(0, min(self.player_pos[1] + self.movement[1], screen_height - self.player_img.get_height()))

def main():
    """Main function"""
    game.init()
    game.camera.init()

    PLAYER_SPEED = 2

    gui = Gui()

    player_images = [game.image.load("Assets/Sprite/Player_Anabelle.png"),  
                     game.image.load("Assets/Sprite/Player_Anabelle_Left.png"), 
                     game.image.load("Assets/Sprite/Player_Anabelle_Right.png")]
    player_main = Player(player_images)

    clock = game.time.Clock()
    run = True
    while run:
        for event in game.event.get():
            if event.type == game.QUIT:
                run = False
            else:
                player_main.handle_event(event, PLAYER_SPEED)

        player_main.update_position(gui.SCREEN_WIDTH, gui.SCREEN_HEIGHT)
        gui.draw(player_main)
        clock.tick(120)

    game.quit()

if __name__ == "__main__":
    main()
