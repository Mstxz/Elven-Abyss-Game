# scenemanager.py
import main

class Scene_Base:
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, pressed_keys):
        pass

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
        self.bg = main.game.image.load("Assets/Sprite/Scene_BG.png")

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == main.game.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.button_rect.collidepoint(mouse_pos):
                    self.switch_to_scene(GameScene())

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        title_text = self.font.render("Elven Abyss", True, (255, 255, 255))
        screen.blit(title_text, (30, 30))
        button_font = main.game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 50)
        button_text = button_font.render("Start Game", 1, (255, 255, 255))
        screen.blit(button_text, (self.button_rect.x + 50, self.button_rect.y + 25))

class PauseScene(Scene_Base):
    def __init__(self):
        super().__init__()
        self.button_rect = main.game.Rect(30, 400, 400, 100)
        self.font = main.game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 120)
        self.bg = main.game.image.load("Assets/Sprite/Scene_BG.png")

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == main.game.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.button_rect.collidepoint(mouse_pos):
                    self.switch_to_scene(GameScene())

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        title_text = self.font.render("Pause", True, (255, 255, 255))
        screen.blit(title_text, (30, 30))
        button_font = main.game.font.Font("Assets/Fonts/Bungee-Regular.ttf", 50)
        button_text = button_font.render("Continue", 1, (255, 255, 255))
        screen.blit(button_text, (self.button_rect.x + 50, self.button_rect.y + 25))

class GameScene(Scene_Base):
    def __init__(self):
        super().__init__()
        self.gui = main.UI.Gui()
        self.mc = main.player.Character()
        self.enemy = main.enemy.Enemy(x=100, y=300)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == main.game.QUIT:
                main.game.quit()
                main.sys.exit()
            elif event.type == main.game.KEYDOWN and event.key == main.game.K_ESCAPE:
                self.switch_to_scene(PauseScene())
            elif event.type == main.game.KEYDOWN and event.key == main.game.K_i:
                self.switch_to_scene(CombatScene())
            else:
                self.mc.handle_event(event)

    def update(self):
        self.mc.update_movement()
        self.mc.update_position(main.UI.SCREEN_WIDTH, main.UI.SCREEEN_HEIGHT)
        self.enemy.update(self.mc.rect)

    def render(self, screen):
        self.gui.draw(self.mc)

class CombatScene(Scene_Base):
    def __init__(self):
        super().__init__()
        self.gui = main.UI.Combat_Gui()
        self.mc = main.player.Character()

    def render(self, screen):
        self.gui.draw(self.mc)