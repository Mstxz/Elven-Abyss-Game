import main

class Enemy:
    def __init__(self, x, y):
        self.ENEMY_SIZE = 40
        self.ENEMY_COLOR = (0,0,255)
        self.ENEMY_SPEED = 2
        self.DETECTION_RADIUS = 300
        self.rect = main.game.Rect(x, y, self.ENEMY_SIZE, self.ENEMY_SIZE)
        self.start_x = x
        self.speed = self.ENEMY_SPEED
        self.direction = 1

    def detect_player(self, player_pos):
        """Detect if the player is within the detection radius."""
        distance_to_player = main.math.hypot(player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery)
        return distance_to_player < self.DETECTION_RADIUS

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
        main.game.draw.rect(surface, self.ENEMY_COLOR, self.rect)