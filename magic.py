"""Player Magic Combat"""
import pygame as game
import math

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
    def __init__(self, x, y, target_x, target_y, speed=20):
        red_square_image = game.Surface((50, 50))
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
