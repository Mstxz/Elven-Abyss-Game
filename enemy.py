"""Enemy"""
import math
import main

class Enemy:
    """Enemy Class"""
    def __init__(self, x, y):
        self.enemy_size = 40
        self.enemy_color = (0,0,255)
        self.enemy_speed = 2
        self.detection_radius = 300
        self.rect = main.game.Rect(x, y, self.enemy_size, self.enemy_size)
        self.start_x = x
        self.speed = self.enemy_speed
        self.direction = 1

    def detect_player(self, player_pos):
        """Detect if the player is within the detection radius."""
        d2player = math.hypot(player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery)
        return d2player < self.detection_radius

    def chase_player(self, player_pos):
        """Chase the player when detected."""
        if player_pos[0] > self.rect.x:
            self.rect.x += self.speed
        elif player_pos[0] < self.rect.x:
            self.rect.x -= self.speed

        if player_pos[1] > self.rect.y:
            self.rect.y += self.speed
        elif player_pos[1] < self.rect.y:
            self.rect.y -= self.speed

    def update(self, player_pos):
        """Update enemy behavior."""
        if self.detect_player(player_pos):
            self.chase_player(player_pos)
        else:
            pass

    def draw(self, surface):
        """Draw Enemy"""
        main.game.draw.rect(surface, self.enemy_color, self.rect)
