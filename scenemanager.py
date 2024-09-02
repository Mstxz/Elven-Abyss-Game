"""Scene Manager"""
import main
import UI
import player
import enemy as mon

class SceneBase:
    """Scene Base Class"""
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, pressed_keys):
        """Process Input"""
        pass

    def update(self):
        """Update"""
        pass

    def render(self, screen):
        """Render Scene"""
        pass

    def switch_to_scene(self, next_scene):
        """Switch to another scene"""
        self.next_scene = next_scene

class TitleScene(SceneBase):
    """Main Menu"""
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

class PauseScene(SceneBase):
    """Pause Scene"""
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

class GameScene(SceneBase):
    """Main Game scene"""
    def __init__(self):
        super().__init__()
        self.gui = UI.Gui()
        self.mc = player.Character()
        self.combat = player.Combat()
        self.game_manager = player.GameManager()

        # Create enemy sprite
        enemy_sprite = main.game.Surface((50, 50))
        enemy_sprite.fill((255, 0, 0))  # Example: red square as enemy sprite

        # Instantiate the enemy
        self.enemy = mon.Enemy(enemy_hp=100, enemy_dmg=10, enemy_sprite=enemy_sprite, x=200, y=200, speed=0)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == main.game.QUIT:
                main.game.quit()
                main.sys.exit()
            elif event.type == main.game.KEYDOWN and event.key == main.game.K_ESCAPE:
                self.switch_to_scene(PauseScene())
            elif event.type == main.game.MOUSEBUTTONDOWN:
                self.combat.shooting(event, self.mc, self.game_manager)
            else:
                self.mc.handle_event(event)

    def update(self):
        self.mc.update_movement()
        self.mc.update_position(UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)
        self.game_manager.update(keys=None)
        self.enemy.update()  # Update the enemy position

    def render(self, screen):
        self.gui.draw(self.mc)  # Draw the GUI and player character
        self.game_manager.render(screen)  # Render other game elements

        # Add this line to draw the enemy on the screen
        self.enemy.draw(screen)

        # Update the display (if not already being done elsewhere in your game loop)
        main.game.display.flip()
