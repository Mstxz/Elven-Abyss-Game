"""Player"""
import main

class Character:
    def __init__(self):
        super().__init__()
        # Player Image Setup
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
            main.game.K_f: False,
            main.game.K_c: False,
            main.game.K_v: False,
            main.game.K_r: False,
            main.game.K_SPACE: False,
        }

        # Player stats
        self.player_hp = 100
        self.player_stamina = 100
        self.combat = Combat()
        self.level = 1
        self.player_exp = 0
        self.player_max_exp = 25 * ((self.level // 3 + 1) ** 2) + 75 * (self.level // 3 + 1)

    def handle_event(self, event):
        def update():
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
        # Horizontal movement
        if self.key_state[main.game.K_a]:
            self.movement[0] = -self.speed
            self.player_img = self.player_imgs[1]  # Left image
        elif self.key_state[main.game.K_d]:
            self.movement[0] = self.speed
            self.player_img = self.player_imgs[2]  # Right image
        else:
            self.movement[0] = 0

        # Vertical movement
        if self.key_state[main.game.K_w]:
            self.movement[1] = -self.speed
            self.player_img = self.player_imgs[3]  # Up image
        elif self.key_state[main.game.K_s]:
            self.movement[1] = self.speed
            self.player_img = self.player_imgs[0]  # Down image
        else:
            self.movement[1] = 0

    def update_position(self, world_width, world_height):
        self.player_pos[0] = max(0, min(self.player_pos[0] + self.movement[0], world_width - self.player_img.get_width()))
        self.player_pos[1] = max(0, min(self.player_pos[1] + self.movement[1], world_height - self.player_img.get_height()))
        self.rect.topleft = self.player_pos

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
            max_exp = 25 * ((level // 3 + 1) ** 2) + 75 * ((level // 3 + 1))

        if key_state[main.game.K_r]:
            exp += 20
        return exp, max_exp, level
