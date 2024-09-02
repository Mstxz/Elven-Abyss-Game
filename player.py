"""Player"""
import main
import magic
import math
import enemy as mon

class Character:
    """Character Class"""
    def __init__(self):
        super().__init__()
        #player sprites here
        self.player_imgs = [
            main.game.image.load("Assets/Sprite/Player_Anabelle.png"),  
            main.game.image.load("Assets/Sprite/Player_Anabelle_Left.png"), 
            main.game.image.load("Assets/Sprite/Player_Anabelle_Right.png"),
            main.game.image.load("Assets/Sprite/Player_Anabelle_Back.png")
        ]
        self.player_img = self.player_imgs[0]
        self.player_pos = [960, 540]
        self.movement = [0, 0]
        self.rect = self.player_img.get_rect()
        self.rect.topleft = self.player_pos

        # Movement Variable
        self.speed = 7
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

        # Player stats
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

    def update_movement(self):
        """Movement Update"""
        if self.key_state[main.game.K_a]:
            self.movement[0] = -self.speed
            self.player_img = self.player_imgs[1]  # Left image
        elif self.key_state[main.game.K_d]:
            self.movement[0] = self.speed
            self.player_img = self.player_imgs[2]  # Right image
        else:
            self.movement[0] = 0
        if self.key_state[main.game.K_w]:
            self.movement[1] = -self.speed
            self.player_img = self.player_imgs[3]  # Up image
        elif self.key_state[main.game.K_s]:
            self.movement[1] = self.speed
            self.player_img = self.player_imgs[0]  # Down image
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
        self.magic_damage = 10  # Example damage value for magic attacks

    def combat_skill(self, key_state, stamina):
        """Handle player skill usage"""
        if key_state[main.game.K_1] and stamina >= 10:
            print("Pew Pew Pew (Magic Attack)")
            stamina -= 10
            # Example: Handle a magic attack (implement details later)
        elif key_state[main.game.K_2] and stamina >= 20:
            print("Smash!!! (Physical Attack)")
            stamina -= 20
            # Example: Handle a physical attack
        elif key_state[main.game.K_3] and stamina >= 50:
            print("Ultimate!!! (Powerful Attack)")
            stamina -= 50
            # Example: Handle an ultimate attack

        if stamina <= 0:
            stamina = 100  # Reset stamina when it runs out (you can adjust this logic)

        return stamina

    def levelling(self, key_state, exp, max_exp, level):
        """Handle player leveling up"""
        if exp >= max_exp:
            exp -= max_exp
            level += 1
            max_exp = 25 * ((level // 3 + 1) ** 2) + 75 * ((level // 3 + 1))
            print(f"Level up! New level: {level}")

        if key_state[main.game.K_r]:
            exp += 20  # Grant experience when pressing 'R' (for testing purposes)

        return exp, max_exp, level

    def shooting(self, event, character, game_manager):
        """Handle player shooting a magic projectile"""
        if event.type == main.game.MOUSEBUTTONDOWN and event.button == 1:
            cursor_x, cursor_y = main.game.mouse.get_pos()
            red_square = magic.Range_Object(character.player_pos[0], character.player_pos[1], cursor_x, cursor_y)
            game_manager.instantiate(red_square)

    def attack(self, player, enemies):
        """Handle melee or ranged attacks on enemies within range"""
        for enemy in enemies:
            distance = self.calculate_distance(player.rect.center, enemy.rect.center)
            if distance <= player.attack_range:  # Assume player has an attack range
                enemy.enemy_hp -= self.magic_damage  # Deal damage to the enemy
                if enemy.enemy_hp <= 0:
                    print("Enemy defeated!")
                    enemies.remove(enemy)  # Remove enemy if defeated

    @staticmethod
    def calculate_distance(pos1, pos2):
        """Helper method to calculate distance between two points"""
        return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

class GameManager:
    def __init__(self):
        self.objects = []  # This includes enemies, projectiles, etc.

    def instantiate(self, game_object):
        self.objects.append(game_object)

    def update(self, keys):
        for obj in self.objects:
            if isinstance(obj, magic.GameObject):
                obj.update()

        # Check for collisions between projectiles and enemies
        for obj in self.objects:
            if isinstance(obj, magic.Range_Object):
                for enemy in [o for o in self.objects if isinstance(o, mon.Enemy)]:
                    if self.check_collision(obj, enemy):
                        enemy.enemy_hp -= 20  # Example damage
                        obj.destroyed = True  # Destroy projectile
                        if enemy.enemy_hp <= 0:
                            self.remove_enemy(enemy)

        # Clean up destroyed objects
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
