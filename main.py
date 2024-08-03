"""main game"""
import pygame as game
import player
import UI

def main():
    """Main function"""
    game.init()
    PLAYER_SPEED = 2

    gui = UI.Gui()

    player_images = [game.image.load("Assets/Sprite/Player_Anabelle.png"),  
                     game.image.load("Assets/Sprite/Player_Anabelle_Left.png"), 
                     game.image.load("Assets/Sprite/Player_Anabelle_Right.png")]
    player_main = player.Player(player_images)

    clock = game.time.Clock()
    run = True
    while run:
        for event in game.event.get():
            if event.type == game.QUIT:
                run = False
            else:
                player_main.handle_event(event, PLAYER_SPEED)

        player_main.update_position(gui.SCREEN_WIDTH, gui.SCREEN_HEIGHT)
        gui.draw(player_main)
        clock.tick(120)

    game.quit()

if __name__ == "__main__":
    main()
