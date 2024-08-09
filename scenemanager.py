"""Scene Manager"""
import main

class Scene_Base:
    """Main base for changing scene"""
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, pressed_keys):
        try:
            pass
        except AttributeError:
            print("Ended")

    def update(self):
        pass

    def render(self, screen):
        pass

    def switch_to_scene(self, next_scene):
        self.next_scene = next_scene

class TitleScene(Scene_Base):
    def __init__(self):
        super().__init__()
        self.button_rect = main.game.Rect(30, 400, 400, 100)
        self.font = main.game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 120)
        self.bg = main.game.image.load("Assets/Sprite/Scene_BG.jpg")
        self.bg = main.game.transform.scale_by(self.bg, 2.5)

    def process_input(self, events):
        for event in events:
            if event.type == main.game.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.button_rect.collidepoint(mouse_pos):
                    self.switch_to_scene(GameScene())


    def render(self, screen):
        screen.blit(self.bg ,(0, 0))
        title_text = self.font.render("Elven Abyss", True, (255, 255, 255))
        screen.blit(title_text, (30, 30))
        
        # Draw the button
        button_font = main.game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 50)  # Load font for the button text
        button_text = button_font.render("Start Game", 1, (255, 255, 255))
        main.game.draw.rect(screen, (0, 0, 0), self.button_rect)
        screen.blit(button_text, (self.button_rect.x + 50, self.button_rect.y + 25))

class GameScene(Scene_Base):
    def __init__(self):
        super().__init__()
        self.gui = main.UI.Gui()  # Initialize the GUI here
        self.mc = main.player.Character()
        self.camera = main.cam.Camera(self.gui.SCREEN_WIDTH, self.gui.SCREEN_HEIGHT, self.gui.WORLD_WIDTH, self.gui.WORLD_HEIGHT)

    def process_input(self, events):
        for event in events:
            if event.type == main.game.QUIT:
                main.game.quit()
                main.sys.exit()
            elif event.type == main.game.KEYDOWN and event.key == main.game.K_ESCAPE:
                self.switch_to_scene(TitleScene())  # Switch to TitleScene when ESC is pressed
            else:
                self.mc.handle_event(event)

    def update(self):
        self.mc.update_position(self.gui.WORLD_WIDTH, self.gui.WORLD_HEIGHT)
        self.camera.update(self.mc)

    def render(self, screen):
        self.gui.draw(self.mc, self.camera)
