"""Scene Manager"""
import main
import UI
import player
import enemy as mon
import random
from math import sqrt
import combat

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
        self.playercombat = player.PlayerCombat()
        self.game_manager = player.GameManager()
        self.combat = combat.Combat()

        # Create enemy sprite
        enemy_sprite = main.game.Surface((50, 50))
        enemy_sprite.fill((255, 0, 0))  # Example: red square as enemy sprite

        # Instantiate the EnemyManager
        self.enemy_manager = mon.EnemyManager()

        # Define spawn area boundaries
        spawn_area_x_min = 200
        spawn_area_x_max = UI.SCREEN_WIDTH - 200
        spawn_area_y_min = 200
        spawn_area_y_max = UI.SCREEN_HEIGHT - 200

        # Spawn multiple enemies at random position
        for i in range(5):
            while True:
                random_x = random.randint(spawn_area_x_min, spawn_area_x_max)
                random_y = random.randint(spawn_area_y_min, spawn_area_y_max)

                player_x, player_y = self.mc.player_pos
                distance = sqrt((random_x - player_x) ** 2 + (random_y - player_y) ** 2)
                
                # Ensure the enemy is at least 300px away from the player
                if distance >= 300:
                    self.enemy_manager.spawn_enemy(enemy_hp=100, enemy_sprite=enemy_sprite, enemy_dmg=10, 
                                                   x=random_x, y=random_y, speed=2)
                    break  # Exit the loop once a valid position is found

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == main.game.QUIT:
                main.game.quit()
                main.sys.exit()
            elif event.type == main.game.KEYDOWN and event.key == main.game.K_ESCAPE:
                self.switch_to_scene(PauseScene())
            elif event.type == main.game.MOUSEBUTTONDOWN:
                self.playercombat.shooting(event, self.mc, self.game_manager)
            else:
                self.mc.handle_event(event)

    def update(self):
        self.enemy_manager.update(self.mc.player_pos)  # Update all enemies
        self.mc.update_movement()
        self.mc.update_position(UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)

        # Update combat (player attacking enemies)
        self.combat.update_combat(self.mc, self.enemy_manager.enemies)

        # Handle player skill usage and leveling
        self.mc.player_stamina = self.mc.combat.combat_skill(self.mc.key_state, self.mc.player_stamina)
        self.mc.player_exp, self.mc.player_max_exp, self.mc.level = self.mc.combat.levelling(
            self.mc.key_state, self.mc.player_exp, self.mc.player_max_exp, self.mc.level)

        self.game_manager.update(keys=None)

    def render(self, screen):
        self.gui.draw(self.mc)
        self.game_manager.render(screen)

        self.enemy_manager.draw(screen)

        main.game.display.flip()
