"""main game"""
import pygame as game
import player
import UI
import sys
import camera as cam

def main():
    """Main function"""
    game.init()

    gui = UI.Gui()
    mc = player.Character()
    camera = cam.Camera(gui.SCREEN_WIDTH, gui.SCREEN_HEIGHT, gui.WORLD_WIDTH, gui.WORLD_HEIGHT)

    clock = game.time.Clock()
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                sys.exit()
            else:
                mc.handle_event(event)

        mc.update_position(gui.WORLD_WIDTH, gui.WORLD_HEIGHT)
        camera.update(mc)
        gui.draw(mc, camera)
        clock.tick(120)

if __name__ == "__main__":
    main()
