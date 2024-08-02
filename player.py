"""Player"""
import main
class Player_animation:
    """Player Animation"""
    player_movement = [
        "Assets/Sprite/Player_Anabelle.png", 
        "Assets/Sprite/Player_Anabelle_Back.png", 
        "Assets/Sprite/Player_Anabelle_Left.png", 
        "Assets/Sprite/Player_Anabelle_Right.png"
    ]

class Player_Main:
    """Player"""
    player_imgs = [main.game.transform.scale_by(main.game.image.load(path), 2) for path in Player_animation.player_movement]
    player_img = player_imgs[0]
    player_pos = [(main.Gui.SCREEN_WIDTH // 2) - (player_img.get_width() // 2), (main.Gui.SCREEN_HEIGHT // 2) - (player_img.get_height() // 2)]
    movement = [0, 0]
    player_max_hp = 100
    player_hp = player_max_hp
