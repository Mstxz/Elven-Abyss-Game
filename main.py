"""pygame test"""
import pygame as game

game.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
PLAYER_SPEED = 1

# Initialize screen
screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game.display.set_caption("Elven Abyss")
icon_image = game.image.load("Assets/Sprite/Sebastian_Icon.png")
game.display.set_icon(icon_image)

# Player
player_img = game.image.load("Assets/Sprite/Player_Anabelle.png")
player_pos = [(SCREEN_WIDTH // 2) - (player_img.get_width()), (SCREEN_HEIGHT // 2) - (player_img.get_height())] # x, y
movement = [0, 0]

# Enemy
enemy_img = game.image.load("Assets/Sprite/36px-Red_Sludge.png")
enemy_pos = (200 - enemy_img.get_width(), (SCREEN_HEIGHT // 2) - (enemy_img.get_height()))

def handle_events():
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
            elif event.key == game.K_d:
                movement[0] = PLAYER_SPEED
        elif event.type == game.KEYUP:
            if event.key in (game.K_a, game.K_d):
                movement[0] = 0
            elif event.key in (game.K_w, game.K_s):
                movement[1] = 0
    return True

def update_player_position():
    player_pos[0] = max(0, min(player_pos[0] + movement[0], SCREEN_WIDTH - player_img.get_width()))
    player_pos[1] = max(0, min(player_pos[1] + movement[1], SCREEN_HEIGHT - player_img.get_height()))

def draw(screen_color):
    screen.fill(screen_color)
    screen.blit(enemy_img, enemy_pos)
    screen.blit(player_img, player_pos)
    game.display.update()

def main():
    """main function"""
    clock = game.time.Clock()
    run = True
    while run:
        run = handle_events()
        update_player_position()
        if abs(player_pos[0] - enemy_pos[0]) < 50 and abs(player_pos[1] - enemy_pos[1]) < 50:
            screen_color = (150, 50 ,50)
        else:
            screen_color = (80, 60 ,100)
        draw(screen_color)
        clock.tick(120)
    game.quit()

main()
