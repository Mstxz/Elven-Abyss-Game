"""Scene Manager"""
import random
from math import sqrt
import main
import UI
import player
import enemy as mon
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
        main.game.mixer.music.load("Assets/Audio/Elven_Abyss_Lobby.mp3")
        main.game.mixer.music.set_volume(0.1)
        main.game.mixer.music.play(-1,0,0)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == main.game.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.button_rect.collidepoint(mouse_pos):
                    main.game.mixer.music.stop()
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

        enemy_sprite = main.game.Surface((50, 50)) #it should be enemy sprite here, btu later na eiei
        enemy_sprite.fill((255, 0, 0))

        self.enemy_manager = mon.EnemyManager()

        spawn_area_x_min = 200
        spawn_area_x_max = UI.SCREEN_WIDTH - 200
        spawn_area_y_min = 200
        spawn_area_y_max = UI.SCREEN_HEIGHT - 200

        for i in range(5):
            while True:
                random_x = random.randint(spawn_area_x_min, spawn_area_x_max)
                random_y = random.randint(spawn_area_y_min, spawn_area_y_max)

                player_x, player_y = self.mc.player_pos
                distance = sqrt((random_x - player_x) ** 2 + (random_y - player_y) ** 2)

                if distance >= 300:
                    self.enemy_manager.spawn_enemy(enemy_hp=100, enemy_sprite=enemy_sprite, enemy_dmg=10, 
                                                   x=random_x, y=random_y, speed=2)
                    break

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
        self.enemy_manager.update(self.mc.player_pos)

        self.mc.update_movement()
        self.mc.update_position(UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)

        self.playercombat.update_projectiles()

        self.enemy_manager.check_collisions(self.playercombat.projectiles)


        self.mc.player_stamina = self.mc.combat.combat_skill(self.mc.key_state, self.mc.player_stamina)
        self.mc.player_exp, self.mc.player_max_exp, self.mc.level = self.mc.combat.levelling(
            self.mc.key_state, self.mc.player_exp, self.mc.player_max_exp, self.mc.level)

        self.game_manager.update(keys=None)


    def render(self, screen):
        self.gui.draw(self.mc)
        self.game_manager.render(screen)

        self.enemy_manager.draw(screen)

        main.game.display.flip()
