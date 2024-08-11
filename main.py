"""main game"""
import pygame as game
import player
import UI
import sys
import enemy
import math
import scenemanager

def main(width, height, fps):
    game.init()
    game.font.init()

    screen = game.display.set_mode((width, height))
    clock = game.time.Clock()

    scene_manager = scenemanager.TitleScene()

    while True:
        pressed_keys = game.key.get_pressed()
        events = game.event.get()

        for event in events:
            if event.type == game.QUIT:
                game.quit()
                sys.exit()
            else:
                scene_manager.process_input([event], pressed_keys)

        scene_manager.update()

        screen.fill((0, 0, 0))
        scene_manager.render(screen)

        game.display.flip()
        clock.tick(fps)

        scene_manager = scene_manager.next_scene

if __name__ == "__main__":
    main(1920, 1080, 120)
