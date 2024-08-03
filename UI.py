"""Main UI"""
import main
class Gui:
    """Gui and Screen"""
    def __init__(self):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1920, 1080
        self.screen = main.game.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        main.game.display.set_caption("Elven Abyss")
        icon_image = main.game.image.load("Assets/Sprite/Sebastian_Icon.png")
        main.game.display.set_icon(icon_image)
        background = main.game.image.load("Assets/Sprite/BG.jpg")
        self.background = main.game.transform.scale(background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw(self, player):
        """Draw everything"""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(player.player_img, player.player_pos)
        main.game.display.update()