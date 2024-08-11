"""Gui"""
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
        self.font = main.game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 30)

        self.rect = main.game.Rect(10, 10, 250, 150)  # Position (10, 10), width 100, height 50
        self.rect_color = (184, 156, 100)  # Color of the rectangle (Red)

    def draw(self, player):
        """Draw UI"""
        text_hp = self.font.render(f"HP : {player.player_hp:02d} / 100", True, (91, 80, 58 ))
        text_sta = self.font.render(f"STA : {player.player_stamina:02d} / 100", True, (91, 80, 58 ))
        text_exp = self.font.render(f"EXP : {player.player_exp:02d} / {player.player_max_exp}", True, (91, 80, 58 ))
        text_level = self.font.render(f"Level : {player.level}", True, (0, 0, 0))

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(player.player_img, player.player_pos)

        main.game.draw.rect(self.screen, self.rect_color, self.rect)

        self.screen.blit(text_hp, (20, 20))
        self.screen.blit(text_sta, (20, 60))
        self.screen.blit(text_exp, (20, 100))
        self.screen.blit(text_level, (1740, 20))
        main.game.display.update()