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

# Load images
player_img = game.image.load("Assets/Sprite/Sebastian_Icon.png")
enemy_img = game.image.load("Assets/Sprite/36px-Red_Sludge.png")

# Player and enemy positions
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
enemy_pos = [200, SCREEN_HEIGHT // 2]
movement = [0, 0]

def handle_events():
    global movement
    for event in game.event.get():
        if event.type == game.QUIT:
            return False
        elif event.type == game.KEYDOWN:
            if event.key == game.K_w:
                movement[1] = -PLAYER_SPEED
            elif event.key == game.K_s:
                movement[1] = PLAYER_SPEED
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

def check_collision():
    return abs(player_pos[0] - enemy_pos[0]) < 50 and abs(player_pos[1] - enemy_pos[1]) < 50

def draw(screen_color):
    screen.fill(screen_color)
    screen.blit(player_img, player_pos)
    screen.blit(enemy_img, enemy_pos)
    game.display.update()

def main():
    clock = game.time.Clock()
    run = True
    while run:
        run = handle_events()
        update_player_position()
        screen_color = (100, 0, 0) if check_collision() else (0, 0, 0)
        draw(screen_color)
        clock.tick(120)
    game.quit()

if __name__ == "__main__":
    main()
