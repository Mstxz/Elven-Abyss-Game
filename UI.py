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
        self.font = main.game.font.Font(None, 72)
        self.text_hp = self.font.render(f"HP : {5:02d} / {100}", True, (150, 0, 220))
        self.text_sta = self.font.render(f"STA : {100:02d} / {100:02d}", True, (255, 180, 0))

    def draw(self, player):
        """Draw UI"""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(player.player_img, player.player_pos)
        self.screen.blit(self.text_hp, (20, 20))
        self.screen.blit(self.text_sta, (20, 75))
        main.game.display.update()
class Stat:
    """Display Player Stat"""
    def __init__(self):
        self.stamina = 100
        self.health_point = 100
