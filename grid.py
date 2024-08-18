import main
import time
import sys
import math

main.game.init()

class Grid:
    def __init__(self, grid_size, space_color):
        self.width = 1920
        self.height = 1080
        self.grid_size = grid_size
        self.rows = 1080 // grid_size
        self.cols = 1920 // grid_size
        self.space_color = space_color
        
        self.screen = main.game.display.set_mode((1920, 1080))
        main.game.display.set_caption("Grid Example")

        self.clock = main.game.time.Clock()
        self.player_size = grid_size
        self.player_pos = [0, 0]
        self.destination_pos = None

    def draw_grid(self):
        """Draw a grid"""
        for x in range(0, self.width, self.grid_size):
            main.game.draw.line(self.screen, (255,255,255), (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            main.game.draw.line(self.screen, (255,255,255), (0, y), (self.width, y))

    def get_grid_pos(self, pos):
        """Get grid position"""
        grid_x = pos[0] // self.grid_size
        grid_y = pos[1] // self.grid_size
        return grid_x, grid_y

    def draw_movement_radius(self):
        """Fill the available grid within the movement radius"""
        radius = 5

        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                grid_x = self.player_pos[0] + x
                grid_y = self.player_pos[1] + y

                if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:

                    if math.sqrt(x ** 2 + y ** 2) <= radius:
                        rect = (grid_x * self.grid_size, grid_y * self.grid_size, self.grid_size, self.grid_size)
                        main.game.draw.rect(self.screen, self.space_color, rect)

    def draw_player(self):
        """Draw player in grid position"""
        rect = main.game.image.load("Assets/Sprite/Player_Anabelle.png")
        self.screen.blit(rect, (self.player_pos[0] * self.grid_size, self.player_pos[1] * self.grid_size))

    def move_towards_destination(self):
        """Move player towards destination in grid steps with a radius limit of 5"""
        distance = math.sqrt((self.destination_pos[0] - self.player_pos[0]) ** 2 + 
                             (self.destination_pos[1] - self.player_pos[1]) ** 2)
        
        if distance <= 5:
            if self.player_pos[0] < self.destination_pos[0]:
                self.player_pos[0] += 1
            elif self.player_pos[0] > self.destination_pos[0]:
                self.player_pos[0] -= 1
            elif self.player_pos[1] < self.destination_pos[1]:
                self.player_pos[1] += 1
            elif self.player_pos[1] > self.destination_pos[1]:
                self.player_pos[1] -= 1

    def run(self):
        while True:
            for event in main.game.event.get():
                if event.type == main.game.QUIT:
                    main.game.quit()
                    sys.exit()

                if event.type == main.game.MOUSEBUTTONDOWN:
                    mouse_pos = main.game.mouse.get_pos()
                    self.destination_pos = self.get_grid_pos(mouse_pos)

            if self.destination_pos:
                if self.player_pos != self.destination_pos:
                    self.move_towards_destination()
                    time.sleep(0.1)

            self.screen.fill((0,200,0))
            self.draw_movement_radius()
            self.draw_grid()
            self.draw_player()
            main.game.display.flip()
            self.clock.tick(120)

if __name__ == "__main__":
    grid = Grid(40, (54, 78, 236))
    grid.run()
