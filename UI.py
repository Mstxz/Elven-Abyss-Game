"""Gui"""
import main

SCREEN_WIDTH, SCREEEN_HEIGHT = 1920, 1080

class Gui:
    """Gui and Screen"""
    def __init__(self):
        self.width, self.height = SCREEN_WIDTH, SCREEEN_HEIGHT
        self.screen = main.game.display.set_mode((self.width, self.height))
        main.game.display.set_caption("Elven Abyss")
        self.icon_image = main.game.image.load("Assets/Sprite/Sebastian_Icon.png")
        main.game.display.set_icon(self.icon_image)
        background = main.game.image.load("Assets/Sprite/BG.jpg")
        self.background = main.game.transform.scale(background, (self.width, self.height))
        self.font = main.game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 30)

        self.rect = main.game.Rect(10, 10, 250, 150)
        self.rect_color = (184, 156, 100)

    def draw(self, player):
        """Draw UI"""
        text_hp = self.font.render(f"HP : {player.player_hp:02d} / {player.player_max_hp}", True, (91, 80, 58 ))
        text_sta = self.font.render(f"STA : {player.player_stamina:02d} / {player.player_max_stamina}", True, (91, 80, 58 ))
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

class Combat_Gui:
    """Combat Gui"""
    def __init__(self) -> None:
        self.width, self.height = SCREEN_WIDTH, SCREEEN_HEIGHT
        self.screen = main.game.display.set_mode((self.width, self.height))
        main.game.display.set_caption("Elven Abyss")
        self.icon_image = main.game.image.load("Assets/Sprite/Sebastian_Icon.png")
        main.game.display.set_icon(self.icon_image)
        background = main.game.image.load("Assets/Sprite/BG.jpg")
        self.background = main.game.transform.scale(background, (self.width, self.height))
        self.font = main.game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 30)
        self.font_h1 = main.game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 70)

    def draw(self, player):
        """Draw UI"""

        bar_width = 300
        bar_height = 40

        player_hp_bar_width = int((player.player_hp / player.player_max_hp) * bar_width)
        # enemy_hp_bar_width = int((enemy.hp / enemy.max_hp) * bar_width)

        main.game.draw.rect(self.screen, (0, 255, 0), (20, 100, player_hp_bar_width, bar_height))  # Green bar
        self.screen.blit(self.font_h1.render("Player", True, (255, 255, 255)), (20, 20))
        self.screen.blit(self.font.render(f"HP : {player.player_hp:03d}", True, (255, 255, 255)), (20, 100))

        # main.game.draw.rect(self.screen, (0, 255, 0), (1580, 60, enemy_hp_bar_width, bar_height))  # Green bar
        self.screen.blit(self.font_h1.render("Enemy 1", True, (255, 255, 255)), (1580, 20))
        # self.screen.blit(self.font.render(f"HP : {enemy.hp:03d}", True, (255, 255, 255)), (1580, 60))

        self.screen.blit(self.font.render(f"STA : {player.player_stamina:03d}", True, (255, 255, 255)), (20, 140))
        # self.screen.blit(self.font.render(f"STA : {enemy.stamina:03d}", True, (255, 255, 255)), (1580, 100))

        main.game.display.update()
