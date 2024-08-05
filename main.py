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

    player_images = [game.image.load("Assets/Sprite/Player_Anabelle.png"),  
                     game.image.load("Assets/Sprite/Player_Anabelle_Left.png"), 
                     game.image.load("Assets/Sprite/Player_Anabelle_Right.png")]
    player_main = player.Player(player_images, player.Combat)

    clock = game.time.Clock()
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                sys.exit()
            else:
                player_main.handle_event(event, PLAYER_SPEED)

        player_main.update_position(gui.SCREEN_WIDTH, gui.SCREEN_HEIGHT)
        gui.draw(player_main)
        clock.tick(120)

if __name__ == "__main__":
    main()
