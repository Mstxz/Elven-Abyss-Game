"""main game"""
import sys
import pygame as game
import scenemanager

def main(width, height, fps):
    """Main game loop"""

    #======================init======================#
    game.init()
    game.font.init()
    game.mixer.init()

    #======================setup and objects======================#
    screen = game.display.set_mode((width, height))
    clock = game.time.Clock()
    scene_manager = scenemanager.TitleScene()

    #======================loop======================#
    while True:
        pressed_keys = game.key.get_pressed()
        events = game.event.get()

        #================event================#
        for event in events:
            if event.type == game.QUIT:
                game.quit()
                sys.exit()
            else:
                scene_manager.process_input([event], pressed_keys)

        scene_manager.update() #update scene

        screen.fill((0, 0, 0))
        scene_manager.render(screen)

        game.display.flip()
        clock.tick(fps)

        scene_manager = scene_manager.next_scene

#======call main loop======#
if __name__ == "__main__":
    main(1280 , 720, 60)
