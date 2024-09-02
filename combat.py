"""Combat System"""
import player
import enemy
from math import sqrt

import player
import enemy
from math import sqrt

class Combat:
    """Combat System Class"""
    def __init__(self):
        self.player_attack_range = 100
        self.enemy_attack_range = 50
        self.player_attack_damage = 20
        self.enemy_attack_damage = 10

    def player_attack(self, player, enemies):
        """Handle the player attacking enemies."""
        for enemy in enemies:
            distance = self.calculate_distance(player.player_pos[0], player.player_pos[1], enemy.x, enemy.y)
            if distance <= self.player_attack_range:
                enemy.enemy_hp -= self.player_attack_damage
                if enemy.enemy_hp <= 0:
                    enemies.remove(enemy)
                    print("Enemy defeated!")

    def enemy_attack(self, player, enemies):
        """Handle enemies attacking the player."""
        for enemy in enemies:
            distance = self.calculate_distance(player.player_pos[0], player.player_pos[1], enemy.x, enemy.y)
            if distance <= self.enemy_attack_range:
                player.player_hp -= self.enemy_attack_damage
                if player.player_hp <= 0:
                    print("Player defeated!")
                    # Handle player defeat (e.g., trigger game over)

    def calculate_distance(self, x1, y1, x2, y2):
        """Calculate the distance between two points (x1, y1) and (x2, y2)."""
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def update_combat(self, player, enemies):
        """Update combat for both the player and enemies."""
        self.player_attack(player, enemies)
        self.enemy_attack(player, enemies)
