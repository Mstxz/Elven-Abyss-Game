"""main game"""
import pygame as game
import player
import UI
import sys

def main():
    """Main function"""
    game.init()
    PLAYER_SPEED = 2

    gui = UI.Gui()

    player_movement_img = [game.image.load("Assets/Sprite/Player_Anabelle.png"),  
                     game.image.load("Assets/Sprite/Player_Anabelle_Left.png"), 
                     game.image.load("Assets/Sprite/Player_Anabelle_Right.png")]
    mc = player.Character(player_movement_img)

    clock = game.time.Clock()
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                sys.exit()
            else:
                mc.handle_event(event, PLAYER_SPEED)

        mc.update_position(gui.SCREEN_WIDTH, gui.SCREEN_HEIGHT)
        gui.draw(mc)
        clock.tick(120)

if __name__ == "__main__":
    main()
