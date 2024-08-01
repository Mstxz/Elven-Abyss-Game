"""main game"""
import pygame as game
import pygame.camera

#initialize zone
game.init()
pygame.camera.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
PLAYER_SPEED = 1

class Gui:
    """Gui and Screen"""
    screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game.display.set_caption("Elven Abyss")
    icon_image = game.image.load("Assets/Sprite/Sebastian_Icon.png") #icon
    game.display.set_icon(icon_image)

    hp_text = game

class Player:
    """Player"""
    player_img = game.image.load("Assets/Sprite/Player_Anabelle.png")
    player_pos = [(SCREEN_WIDTH // 2) - (player_img.get_width()), (SCREEN_HEIGHT // 2) - (player_img.get_height())] # x, y
    movement = [0, 0]
    player_max_hp = 100
    player_hp = player_max_hp

def handle_events():
    """similar to void Update() in unity"""
    for event in game.event.get():
        if event.type == game.QUIT:
            return False
        elif event.type == game.KEYDOWN:
            match event.key:
                case game.K_w:
                    Player.movement[1] = -PLAYER_SPEED
                    Player.player_img = game.image.load("Assets/Sprite/Player_Anabelle_Back.png")
                case game.K_s:
                    Player.movement[1] = PLAYER_SPEED
                    Player.player_img = game.image.load("Assets/Sprite/Player_Anabelle.png")
                case game.K_a:
                    Player.movement[0] = -PLAYER_SPEED
                    Player.player_img = game.image.load("Assets/Sprite/Player_Anabelle_Left.png")
                case game.K_d:
                    Player.movement[0] = PLAYER_SPEED
                    Player.player_img = game.image.load("Assets/Sprite/Player_Anabelle_Right.png")
        elif event.type == game.KEYUP:
            if event.key in (game.K_a, game.K_d):
                Player.movement[0] = 0
            elif event.key in (game.K_w, game.K_s):
                Player.movement[1] = 0
    return True

def update_player_position():
    """update player position everytime"""
    Player.player_pos[0] = max(0, min(Player.player_pos[0] + Player.movement[0], SCREEN_WIDTH - Player.player_img.get_width()))
    Player.player_pos[1] = max(0, min(Player.player_pos[1] + Player.movement[1], SCREEN_HEIGHT - Player.player_img.get_height()))

def draw(screen_color):
    """draw everything"""
    Gui.screen.fill(screen_color)
    Gui.screen.blit(Player.player_img, Player.player_pos)
    game.display.update()

def main():
    """main function"""
    clock = game.time.Clock()
    run = True
    while run:
        run = handle_events()
        update_player_position()
        draw((0, 0, 0))
        clock.tick(120)
    game.quit()

main()
