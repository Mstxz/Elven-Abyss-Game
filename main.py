"""main pygame"""
import pygame as game
import pygame.camera

# Initialize Pygame
game.init()
pygame.camera.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
PLAYER_SPEED = 2

class Gui:
    """Gui and Screen"""
    screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game.display.set_caption("Elven Abyss")
    icon_image = game.image.load("Assets/Sprite/Sebastian_Icon.png")
    game.display.set_icon(icon_image)
    background = game.image.load("Assets/Sprite/BG.jpg")
    background = game.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Player:
    """Player"""
    player_anim_paths = [
        "Assets/Sprite/Player_Anabelle.png", 
        "Assets/Sprite/Player_Anabelle_Back.png", 
        "Assets/Sprite/Player_Anabelle_Left.png", 
        "Assets/Sprite/Player_Anabelle_Right.png"
    ]
    player_imgs = [game.transform.scale_by(game.image.load(path), 1.5) for path in player_anim_paths]
    player_img = player_imgs[0]
    player_pos = [(SCREEN_WIDTH // 2) - (player_img.get_width() // 2), (SCREEN_HEIGHT // 2) - (player_img.get_height() // 2)]
    movement = [0, 0]
    player_max_hp = 100
    player_hp = player_max_hp

pressed_keys = set()

def handle_events():
    """Event handling similar to Unity's Update() method"""
    global pressed_keys

    key_down_actions = {
        game.K_w: (0, -PLAYER_SPEED, 1),
        game.K_s: (0, PLAYER_SPEED, 0),
        game.K_a: (-PLAYER_SPEED, 0, 2),
        game.K_d: (PLAYER_SPEED, 0, 3)
    }

    for event in game.event.get():
        if event.type == game.QUIT:
            return False
        elif event.type == game.KEYDOWN:
            if event.key in key_down_actions:
                dx, dy, img_index = key_down_actions[event.key]
                Player.movement[0] += dx
                Player.movement[1] += dy
                pressed_keys.add(event.key)
                Player.player_img = Player.player_imgs[img_index]
        elif event.type == game.KEYUP:
            if event.key in key_down_actions:
                dx, dy, _ = key_down_actions[event.key]
                Player.movement[0] -= dx
                Player.movement[1] -= dy
                pressed_keys.discard(event.key)

                # Update player animation based on the highest priority key still pressed
                for key in key_down_actions:
                    if key in pressed_keys:
                        _, _, img_index = key_down_actions[key]
                        Player.player_img = Player.player_imgs[img_index]
                        break
    return True



def update_player_position():
    """Update player position"""
    Player.player_pos[0] = max(0, min(Player.player_pos[0] + Player.movement[0], SCREEN_WIDTH - Player.player_img.get_width()))
    Player.player_pos[1] = max(0, min(Player.player_pos[1] + Player.movement[1], SCREEN_HEIGHT - Player.player_img.get_height()))

def draw(screen_color):
    """Draw everything"""
    Gui.screen.fill(screen_color)
    Gui.screen.blit(Gui.background, (0, 0))
    Gui.screen.blit(Player.player_img, Player.player_pos)
    game.display.update()

def main():
    """Main function"""
    clock = game.time.Clock()
    run = True
    while run:
        run = handle_events()
        update_player_position()
        draw((0, 0, 0))
        clock.tick(120)
    game.quit()

if __name__ == "__main__":
    main()
