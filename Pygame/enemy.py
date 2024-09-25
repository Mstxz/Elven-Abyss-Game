"""Enemy Manager"""
from math import sqrt

class Enemy:
    """Enemy Class"""
    def __init__(self, enemy_hp, enemy_sprite, enemy_dmg, x, y, speed):
        self.enemy_sprite = enemy_sprite
        self.enemy_hp = enemy_hp
        self.enemy_dmg = enemy_dmg
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = self.enemy_sprite.get_rect(topleft=(self.x, self.y))

    def move(self, dx, dy):
        """Move the enemy by dx and dy."""
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

    def track_player(self, player_pos):
        """Track the player if within a certain distance."""
        distance = sqrt((player_pos[0] - self.x) ** 2 + (player_pos[1] - self.y) ** 2)

        # Tracking the Player
        if 100 <= distance < 1000: # change the tracking position here (min < position < max)
            dx = player_pos[0] - self.x
            dy = player_pos[1] - self.y
            length = sqrt(dx ** 2 + dy ** 2)

            if length != 0:
                dx = (dx / length) * self.speed
                dy = (dy / length) * self.speed
            
            self.move(dx, dy)

        if distance <= 200:
            # Example: Implement attack logic here
            pass

    def take_damage(self, damage):
        """Apply damage to the enemy."""
        self.enemy_hp -= damage
        if self.enemy_hp <= 0:
            return True  # Return True if enemy is dead
        return False

    def update(self, player_pos):
        """Update the enemy's position by tracking the player."""
        self.track_player(player_pos)

    def draw(self, screen):
        """Draw the enemy sprite at the current position."""
        screen.blit(self.enemy_sprite, self.rect.topleft)


class EnemyManager:
    """Enemy Manager Class"""
    def __init__(self):
        self.enemies = []
        self.max_enemies = 5

    def spawn_enemy(self, enemy_hp, enemy_sprite, enemy_dmg, x, y, speed):
        """Spawn a new enemy if the current count is less than the maximum."""
        if len(self.enemies) < self.max_enemies:
            enemy = Enemy(enemy_hp, enemy_sprite, enemy_dmg, x, y, speed)
            self.enemies.append(enemy)

    def update(self, player_pos):
        """Update all enemies."""
        for enemy in self.enemies:
            enemy.update(player_pos)

    def draw(self, screen):
        """Draw all enemies."""
        for enemy in self.enemies:
            enemy.draw(screen)

    def remove_enemy(self, enemy):
        """Remove an enemy from the list."""
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def check_collisions(self, projectiles):
        """Check for collisions between enemies and projectiles."""
        for enemy in self.enemies:
            for projectile in projectiles:
                if enemy.rect.colliderect(projectile.rect):
                    if enemy.take_damage(20):
                        self.remove_enemy(enemy)
                        print("dead")
                    projectiles.remove(projectile)
