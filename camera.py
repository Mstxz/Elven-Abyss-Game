"""Camera"""
import main

class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.camera = main.game.Rect(0, 0, width, height)
        self.width = world_width
        self.height = world_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.camera.width / 2)
        y = -target.rect.centery + int(self.camera.height / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - self.camera.width), x)  # right
        y = max(-(self.height - self.camera.height), y)  # bottom

        self.camera = main.game.Rect(x, y, self.camera.width, self.camera.height)
