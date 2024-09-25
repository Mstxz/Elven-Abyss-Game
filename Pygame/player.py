"""Player"""
import math
import time
import main
import magic
import enemy as mon

class Character:
    """Character Class"""
    def __init__(self):
        super().__init__()
        #========================Player Sprites======================#
        self.player_imgs = {
            'Front': main.game.image.load("Assets/Sprite/Player_Anabelle.png"),  
            'Left': main.game.image.load("Assets/Sprite/Player_Anabelle_Left.png"), 
            'Right': main.game.image.load("Assets/Sprite/Player_Anabelle_Right.png"),
            'Back': main.game.image.load("Assets/Sprite/Player_Anabelle_Back.png")
        }

        self.player_img = self.player_imgs['Front']
        self.player_pos = [960, 540]
        self.movement = [0, 0]
        self.rect = self.player_img.get_rect()
        self.rect.topleft = self.player_pos

        #========================Interaction Keys=========================#
        self.key_state = {
            main.game.K_w: False,
            main.game.K_a: False,
            main.game.K_s: False,
            main.game.K_d: False,
            main.game.K_1: False,
            main.game.K_2: False,
            main.game.K_3: False,
            main.game.K_r: False,
            main.game.K_1: False,
            main.game.K_2: False,
            main.game.K_SPACE: False,
        }
        #========================Player Stats======================#
        self.movement_speed = 7
        self.player_max_hp = 100
        self.player_hp = self.player_max_hp
        self.player_max_stamina = 100
        self.player_stamina = self.player_max_stamina
        self.combat = PlayerCombat()
        self.level = 1
        self.player_exp = 0
        self.player_max_exp = 25 * ((self.level // 3 + 1) ** 2) + 75 * (self.level // 3 + 1)

    def handle_event(self, event):
        """Event Handle"""
        def update():
            """Update anything"""
            self.update_movement()
            self.player_stamina = self.combat.combat_skill(self.key_state, self.player_stamina)
            self.player_exp, self.player_max_exp, self.level = self.combat.levelling(self.key_state, self.player_exp, self.player_max_exp, self.level)

        if event.type == main.game.KEYDOWN:
            if event.key in self.key_state:
                self.key_state[event.key] = True
                update()
        elif event.type == main.game.KEYUP:
            if event.key in self.key_state:
                self.key_state[event.key] = False
                update()

    #======================Update Movement=========================#
    def update_movement(self):
        """Movement Update"""
        if self.key_state[main.game.K_a]:
            self.movement[0] = -self.movement_speed
            self.player_img = self.player_imgs['Left']
        elif self.key_state[main.game.K_d]:
            self.movement[0] = self.movement_speed
            self.player_img = self.player_imgs['Right']
        else:
            self.movement[0] = 0
        if self.key_state[main.game.K_w]:
            self.movement[1] = -self.movement_speed
            self.player_img = self.player_imgs['Back']
        elif self.key_state[main.game.K_s]:
            self.movement[1] = self.movement_speed
            self.player_img = self.player_imgs['Front']
        else:
            self.movement[1] = 0

    def update_position(self, world_width, world_height):
        """Player Position Update"""
        self.player_pos[0] = max(0, min(self.player_pos[0] + self.movement[0],
                                world_width - self.player_img.get_width()))
        self.player_pos[1] = max(0, min(self.player_pos[1] + self.movement[1],
                                world_height - self.player_img.get_height()))
        self.rect.topleft = self.player_pos

class PlayerCombat:
    """Combat Class for the Player"""

    def __init__(self):
        self.magic_damage = 10
        self.cooldowns = {
            "magic": 0,
            "physical": 0,
            "ultimate": 0,
        }
        self.cooldown_durations = {
            "magic": 5,
            "physical": 15,
            "ultimate": 30,
        }
        self.last_time = time.time()
        self.projectiles = []

    def update_cooldowns(self):
        """Update cooldown timers based on time elapsed."""
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        for key in self.cooldowns:
            if self.cooldowns[key] > 0:
                self.cooldowns[key] -= elapsed_time
                self.cooldowns[key] = max(0, self.cooldowns[key])
        self.last_time = current_time

    def combat_skill(self, key_state, stamina):
        """Handle player skill usage with cooldowns"""
        self.update_cooldowns()

        if key_state[main.game.K_1] and stamina >= 10 and self.cooldowns["magic"] == 0:
            print("Pew Pew Pew (Magic Attack)")
            stamina -= 10
            self.cooldowns["magic"] = self.cooldown_durations["magic"]
        elif key_state[main.game.K_2] and stamina >= 20 and self.cooldowns["physical"] == 0:
            print("Smash!!! (Physical Attack)")
            stamina -= 20
            self.cooldowns["physical"] = self.cooldown_durations["physical"]
        elif key_state[main.game.K_3] and stamina >= 50 and self.cooldowns["ultimate"] == 0:
            print("Ultimate!!! (Powerful Attack)")
            stamina -= 50
            self.cooldowns["ultimate"] = self.cooldown_durations["ultimate"]

        if stamina <= 0:
            stamina = 100

        return stamina

    def levelling(self, key_state, exp, max_exp, level):
        """Handle player leveling up"""
        if exp >= max_exp:
            exp -= max_exp
            level += 1
            max_exp = 25 * ((level // 3 + 1) ** 2) + 75 * ((level // 3 + 1))
            print(f"Level up! New level: {level}")

        if key_state[main.game.K_r]:
            exp += 20

        return exp, max_exp, level

    def shooting(self, event, character, game_manager):
        """Handle player shooting a magic projectile"""
        if event.type == main.game.MOUSEBUTTONDOWN and event.button == 1:
            cursor_x, cursor_y = main.game.mouse.get_pos()
            red_square = magic.Range_Object(character.player_pos[0], character.player_pos[1], cursor_x, cursor_y)
            self.projectiles.append(red_square)
            game_manager.instantiate(red_square)

    def update_projectiles(self):
        """Update all projectiles and remove any that are destroyed."""
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.destroyed:
                self.projectiles.remove(projectile)

    def attack(self, player, enemies):
        """Handle melee or ranged attacks on enemies within range"""
        for enemy in enemies:
            distance = self.calculate_distance(player.rect.center, enemy.rect.center)
            if distance <= player.attack_range:
                enemy.enemy_hp -= self.magic_damage
                if enemy.enemy_hp <= 0:
                    print("Enemy defeated!")
                    enemies.remove(enemy)

    @staticmethod
    def calculate_distance(pos1, pos2):
        """Helper method to calculate distance between two points"""
        return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

class GameManager:
    def __init__(self):
        self.objects = []

    def instantiate(self, game_object):
        self.objects.append(game_object)

    def update(self, keys):
        for obj in self.objects:
            if isinstance(obj, magic.GameObject):
                obj.update()

        for obj in self.objects:
            if isinstance(obj, magic.Range_Object):
                for enemy in [o for o in self.objects if isinstance(o, mon.Enemy)]:
                    if self.check_collision(obj, enemy):
                        enemy.enemy_hp -= 20
                        obj.destroyed = True
                        if enemy.enemy_hp <= 0:
                            self.remove_enemy(enemy)

        self.objects = [obj for obj in self.objects if not obj.destroyed]

    def render(self, screen):
        for obj in self.objects:
            obj.render(screen)

    def check_collision(self, obj1, obj2):
        """Check if obj1 and obj2 collide."""
        return obj1.rect.colliderect(obj2.rect)

    def remove_enemy(self, enemy):
        """Remove an enemy from the list."""
        if enemy in self.objects:
            self.objects.remove(enemy)
