"""Player Magic Combat"""
import pygame as game
import math
import UI

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

class Range_Object(GameObject):
    def __init__(self, x, y, target_x, target_y):
        fireball = game.Surface((20, 20))
        fireball.fill((0, 250, 100))
        super().__init__(x, y, fireball)
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 10
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
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

        # Check if the projectile is off-screen
        if self.x < 0 or self.x > UI.SCREEN_WIDTH or self.y < 0 or self.y > UI.SCREEN_HEIGHT:
            self.destroyed = True

        self.rect.topleft = (self.x, self.y)
