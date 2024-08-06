"""Player"""
import main

class Character:
    """Character class"""
    def __init__(self, player_images):
        # Player position
        self.player_imgs = player_images
        self.player_img = self.player_imgs[0]
        self.player_pos = [960, 540]
        #movement
        self.movement = [0, 0]
        self.velocity_y = 0
        self.gravity = 1
        self.jump_strength = -20
        self.on_ground = True
        #set the keys in here
        self.key_state = {
            main.game.K_a: False,
            main.game.K_d: False,
            main.game.K_f: False,  # skill 1
            main.game.K_c: False,  # skill 2
            main.game.K_v: False,  # skill 3
            main.game.K_r: False,
            main.game.K_SPACE: False,
        }
        #player stat
        self.player_hp = 100
        self.player_stamina = 100
        self.combat = Combat()
        self.level = 1
        self.player_exp = 0
        self.player_max_exp = 25 * (self.level ** 2) + 75 * (self.level)

    def handle_event(self, event, speed):
        """Handle player input"""
        def update():
            self.update_movement(speed)
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

    def update_movement(self, speed):
        """Update movement"""
        # Horizontal movement
        if self.key_state[main.game.K_a] and self.key_state[main.game.K_d]:
            self.movement[0] = 0
            self.player_img = self.player_imgs[0]
        elif self.key_state[main.game.K_a]:
            self.movement[0] = -speed
            self.player_img = self.player_imgs[1]
        elif self.key_state[main.game.K_d]:
            self.movement[0] = speed
            self.player_img = self.player_imgs[2]
        else:
            self.movement[0] = 0
            self.player_img = self.player_imgs[0]

        # Jump logic
        if self.key_state[main.game.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

    def update_position(self, screen_width, screen_height):
        """Update player position"""
        self.velocity_y += self.gravity
        self.movement[1] = self.velocity_y
        self.player_pos[0] = max(0, min(self.player_pos[0] + self.movement[0], screen_width - self.player_img.get_width()))
        self.player_pos[1] = min(self.player_pos[1] + self.movement[1], screen_height - self.player_img.get_height())

        if self.player_pos[1] >= screen_height - self.player_img.get_height():
            self.player_pos[1] = screen_height - self.player_img.get_height()
            self.velocity_y = 0
            self.on_ground = True

class Combat:
    """Combat Class"""
    def __init__(self):
        self.magic_damage = -10

    def combat_skill(self, key_state, stamina):
        """Weapon Skill"""
        if key_state[main.game.K_f] and stamina >= 10:
            print("Pew Pew Pew")
            stamina -= 10
        elif key_state[main.game.K_c] and stamina >= 20:
            print("Smash!!!")
            stamina -= 20
        elif key_state[main.game.K_v] and stamina >= 50:
            print("Ultimate!!!")
            stamina -= 50

        if stamina <= 0:
            stamina = 100
        return stamina

    def levelling(self, key_state, exp, max_exp, level):
        if exp >= max_exp:
            exp -= max_exp
            level += 1
            max_exp = 25 * (level ** 2) + 75 * (level)

        if key_state[main.game.K_r]:
            exp += 20
        return exp, max_exp, level
