import main

class Player:
    """Player class"""
    def __init__(self, player_images, magic_combat):
        self.player_imgs = player_images
        self.player_img = self.player_imgs[0]
        self.player_pos = [960, 540]
        self.movement = [0, 0]
        self.key_state = {
            main.game.K_a: False,
            main.game.K_d: False,
            main.game.K_1: False,
        }
        self.magic_combat = magic_combat

    def handle_event(self, event, speed):
        """Handle player input"""
        if event.type == main.game.KEYDOWN:
            if event.key in self.key_state:
                self.key_state[event.key] = True
                self.update_movement(speed)
                self.magic_combat.mage_combat(self.key_state)
        elif event.type == main.game.KEYUP:
            if event.key in self.key_state:
                self.key_state[event.key] = False
                self.update_movement(speed)
                self.magic_combat.mage_combat(self.key_state)

    def update_movement(self, speed):
        """Update movement"""
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

    def update_position(self, screen_width, screen_height):
        """Update player position"""
        self.player_pos[0] = max(0, min(self.player_pos[0] + self.movement[0], screen_width - self.player_img.get_width()))
        self.player_pos[1] = max(0, min(self.player_pos[1] + self.movement[1], screen_height - self.player_img.get_height()))

class MagicCombat:
    """Magic Combat"""
    def __init__(self):
        self.magic_damage = -10
        
    def mage_combat(self, key_state):
        """Magic weapon"""
        if key_state[main.game.K_1]:
            print("Pew Pew Pew")
