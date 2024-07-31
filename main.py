"""pygame test"""
import pygame as game

game.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
PLAYER_SPEED = 1

# Screen
screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game.display.set_caption("Elven Abyss")
icon_image = game.image.load("Assets/Sprite/Sebastian_Icon.png")
game.display.set_icon(icon_image)

# Player
player_img = game.image.load("Assets/Sprite/Player_Anabelle.png")
player_pos = [(SCREEN_WIDTH // 2) - (player_img.get_width()), (SCREEN_HEIGHT // 2) - (player_img.get_height())] # x, y
movement = [0, 0]

def handle_events():
    """similat to void Update() in unity"""
    global movement
    global player_img
    for event in game.event.get():
        if event.type == game.QUIT:
            return False
        elif event.type == game.KEYDOWN:
            if event.key == game.K_w:
                movement[1] = -PLAYER_SPEED
                player_img = game.image.load("Assets/Sprite/Player_Anabelle_Back.png")
            elif event.key == game.K_s:
                movement[1] = PLAYER_SPEED
                player_img = game.image.load("Assets/Sprite/Player_Anabelle.png")
            elif event.key == game.K_a:
                movement[0] = -PLAYER_SPEED
                player_img = game.image.load("Assets/Sprite/Player_Anabelle_Left.png")
            elif event.key == game.K_d:
                movement[0] = PLAYER_SPEED
                player_img = game.image.load("Assets/Sprite/Player_Anabelle_Right.png")
        elif event.type == game.KEYUP:
            if event.key in (game.K_a, game.K_d):
                movement[0] = 0
            elif event.key in (game.K_w, game.K_s):
                movement[1] = 0
    return True

def update_player_position():
    """update player position everytime"""
    player_pos[0] = max(0, min(player_pos[0] + movement[0], SCREEN_WIDTH - player_img.get_width()))
    player_pos[1] = max(0, min(player_pos[1] + movement[1], SCREEN_HEIGHT - player_img.get_height()))

def draw(screen_color):
    """draw everything"""
    screen.fill(screen_color)
    screen.blit(player_img, player_pos)
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
