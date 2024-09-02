"""Test for smth, nothing interest here"""
import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1920, 1080))

class GameObject:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.destroyed = False

    def update(self, keys=None):
        pass

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

class RedSquare(GameObject):
    def __init__(self, x, y, target_x, target_y, speed=5):
        red_square_image = pygame.Surface((50, 50))
        red_square_image.fill((255, 0, 0))
        super().__init__(x, y, red_square_image)
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0

    def update(self):
        if math.hypot(self.target_x - self.x, self.target_y - self.y) > self.speed:
            self.x += self.velocity_x
            self.y += self.velocity_y
        else:
            self.x = self.target_x
            self.y = self.target_y
            self.destroyed = True
        self.rect.topleft = (self.x, self.y)

class Character(GameObject):
    def __init__(self):
        self.player_imgs = [
            pygame.image.load("Assets/Sprite/Player_Anabelle.png"),
            pygame.image.load("Assets/Sprite/Player_Anabelle_Left.png"),
            pygame.image.load("Assets/Sprite/Player_Anabelle_Right.png"),
            pygame.image.load("Assets/Sprite/Player_Anabelle_Back.png")
        ]
        self.player_img = self.player_imgs[0]
        self.player_pos = [960, 540]
        self.movement = [0, 0]
        super().__init__(self.player_pos[0], self.player_pos[1], self.player_img)
        self.speed = 7
        self.key_state = {
            pygame.K_w: False,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: False,
            pygame.K_1: False,
            pygame.K_2: False,
            pygame.K_3: False,
            pygame.K_r: False,
            pygame.K_SPACE: False,
        }
        self.player_max_hp = 100
        self.player_hp = self.player_max_hp
        self.player_max_stamina = 100
        self.player_stamina = self.player_max_stamina
        self.combat = Combat()
        self.level = 1
        self.player_exp = 0
        self.player_max_exp = 25 * ((self.level // 3 + 1) ** 2) + 75 * (self.level // 3 + 1)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_state:
                self.key_state[event.key] = True
                self.update()
        elif event.type == pygame.KEYUP:
            if event.key in self.key_state:
                self.key_state[event.key] = False
                self.update()

    def update(self):
        self.update_movement()
        self.player_stamina = self.combat.combat_skill(self.key_state, self.player_stamina)
        self.player_exp, self.player_max_exp, self.level = self.combat.levelling(self.key_state, self.player_exp, self.player_max_exp, self.level)
        self.update_position(1920, 1080)

    def update_movement(self):
        if self.key_state[pygame.K_a]:
            self.movement[0] = -self.speed
            self.player_img = self.player_imgs[1]
        elif self.key_state[pygame.K_d]:
            self.movement[0] = self.speed
            self.player_img = self.player_imgs[2]
        else:
            self.movement[0] = 0
        if self.key_state[pygame.K_w]:
            self.movement[1] = -self.speed
            self.player_img = self.player_imgs[3]
        elif self.key_state[pygame.K_s]:
            self.movement[1] = self.speed
            self.player_img = self.player_imgs[0]
        else:
            self.movement[1] = 0

    def update_position(self, world_width, world_height):
        self.player_pos[0] = max(0, min(self.player_pos[0] + self.movement[0], world_width - self.player_img.get_width()))
        self.player_pos[1] = max(0, min(self.player_pos[1] + self.movement[1], world_height - self.player_img.get_height()))
        self.rect.topleft = self.player_pos

class Combat:
    def __init__(self):
        self.magic_damage = -10

    def combat_skill(self, key_state, stamina):
        if key_state[pygame.K_1] and stamina >= 10:
            print("Pew Pew Pew")
            stamina -= 10
        elif key_state[pygame.K_2] and stamina >= 20:
            print("Smash!!!")
            stamina -= 20
        elif key_state[pygame.K_3] and stamina >= 50:
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

        if key_state[pygame.K_r]:
            exp += 20
        return exp, max_exp, level

class GameManager:
    def __init__(self):
        self.objects = []

    def instantiate(self, game_object):
        self.objects.append(game_object)

    def update(self, keys):
        for obj in self.objects:
            if isinstance(obj, Character):
                obj.update()
            else:
                obj.update()
        self.objects = [obj for obj in self.objects if not obj.destroyed]

    def render(self, screen):
        for obj in self.objects:
            obj.render(screen)

character = Character()
game_manager = GameManager()
game_manager.instantiate(character)

running = True
while running:
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        character.handle_event(event)

    game_manager.update(keys)
    screen.fill((0, 0, 0))
    game_manager.render(screen)
    pygame.display.flip()

pygame.quit()
