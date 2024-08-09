import main
import pygame as game

class Portal:
    def __init__(self, portal_type, position):
        self.portal_type = portal_type  # e.g., 'combat', 'event', 'treasure'
        self.position = position  # (x, y) coordinates on the screen
        self.sprite = self.load_sprite(portal_type)

    def load_sprite(self, portal_type):
        # Load the appropriate sprite based on the portal type
        if portal_type == 'combat':
            return game.image.load('combat_portal.png')
        elif portal_type == 'event':
            return game.image.load('event_portal.png')
        # Add other portal types as needed

    def draw(self, screen):
        # Draw the portal on the screen at its position
        screen.blit(self.sprite, self.position)

    def interact(self, player):
        # Logic for player interaction
        if self.is_player_near(player):
            return self.portal_type  # Return the type of room to load next

    def is_player_near(self, player):
        # Check if the player is close enough to interact with the portal
        return game.Rect(self.position, self.sprite.get_size()).colliderect(player.rect)

class Room:
    def __init__(self, room_type):
        self.room_type = room_type
        self.portals = self.generate_portals()

    def generate_portals(self):
        # Create portals for the room
        portals = []
        portals.append(Portal('combat', (100, 200)))
        portals.append(Portal('event', (400, 200)))
        # Add more portals with different types and positions
        return portals

    def draw(self, screen):
        # Draw the room and its portals
        for portal in self.portals:
            portal.draw(screen)

    def handle_portal_interaction(self, player):
        # Check if the player interacts with any portal
        for portal in self.portals:
            next_room_type = portal.interact(player)
            if next_room_type:
                return next_room_type
