"""main game"""
import pygame as game
import player
import UI
import sys
import enemy
import camera as cam
import scenemanager

def main(width, height, fps):
    game.init()  # Initialize Pygame
    game.font.init()  # Initialize the font module explicitly
    
    screen = game.display.set_mode((width, height))
    clock = game.time.Clock()
    
    # Initialize the TitleScene here after pygame initialization
    active_scene = scenemanager.TitleScene()
    
    while active_scene is not None:
        pressed_keys = game.key.get_pressed()
        
        filtered_events = []
        for event in game.event.get():
            if event.type == game.QUIT:
                active_scene = None
            else:
                filtered_events.append(event)
        
        active_scene.process_input(filtered_events)
        active_scene.update()
        active_scene.render(screen)
        
        active_scene = active_scene.next_scene
        
        game.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main(1920, 1080, 120)
