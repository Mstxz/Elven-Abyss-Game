"""Gui"""
import pygame as game

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

class Gui:
    """Gui and Screen"""
    def __init__(self):
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen = game.display.set_mode((self.width, self.height))
        game.display.set_caption("Elven Abyss")
        self.icon_image = game.image.load("Assets/Sprite/Sebastian_Icon.png")
        game.display.set_icon(self.icon_image)
        background = game.image.load("Assets/Sprite/BG.jpg")
        self.background = game.transform.scale(background, (self.width, self.height))
        self.font = game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 30)

        self.rect = game.Rect(10, 10, 250, 150)
        self.rect_color = (184, 156, 100)

    def draw(self, player):
        """Draw UI"""
        text_hp = self.font.render(f"HP : {player.player_hp:02d}/{player.player_max_hp}",
                                   True, (91, 80, 58 ))
        text_sta =self.font.render(f"STA : {player.player_stamina:02d}/{player.player_max_stamina}",
                                    True, (91, 80, 58 ))
        text_exp = self.font.render(f"EXP : {player.player_exp:02d}/{player.player_max_exp}",
                                    True, (91, 80, 58 ))
        text_level = self.font.render(f"Level : {player.level}", True, (255, 255, 255))

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(player.player_img, player.player_pos)

        game.draw.rect(self.screen, self.rect_color, self.rect)

        self.screen.blit(text_hp, (20, 20))
        self.screen.blit(text_sta, (20, 60))
        self.screen.blit(text_exp, (20, 100))
        self.screen.blit(text_level, (1740, 20))
        game.display.update()
