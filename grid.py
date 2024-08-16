"""Grid"""
import main
import time
import sys

main.game.init()

WIDTH, HEIGHT = 1920, 1080
GRID_SIZE = 40
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

screen = main.game.display.set_mode((WIDTH, HEIGHT))
main.game.display.set_caption("Grid Example")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PLAYER_COLOR = (0, 128, 255)

clock = main.game.time.Clock()

player_size = GRID_SIZE
player_pos = [0, 0]
destination_pos = None

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        main.game.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        main.game.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def get_grid_pos(pos):
    grid_x = pos[0] // GRID_SIZE
    grid_y = pos[1] // GRID_SIZE
    return grid_x, grid_y

def draw_player(grid_pos):
    available_dest = main.game.Rect(grid_pos[0] * (GRID_SIZE - (grid_pos[0] - 2)), grid_pos[1] * (GRID_SIZE - (grid_pos[1] - 2)), player_size * 5, player_size * 5)
    rect = main.game.Rect(grid_pos[0] * GRID_SIZE, grid_pos[1] * GRID_SIZE, player_size, player_size)
    main.game.draw.rect(screen, YELLOW, available_dest)
    main.game.draw.rect(screen, PLAYER_COLOR, rect)

def move_towards_destination(player_pos, destination_pos):
    if player_pos[0] != destination_pos[0]:
        if abs(destination_pos[0] - player_pos[0]) > 5 or abs(destination_pos[1] - player_pos[1]) > 5:
            pass
        else:
            if player_pos[0] < destination_pos[0]:
                player_pos[0] += 1
            elif player_pos[0] > destination_pos[0]:
                player_pos[0] -= 1
    elif player_pos[1] != destination_pos[1]:
        if abs(destination_pos[0] - player_pos[0]) > 5 or abs(destination_pos[1] - player_pos[1]) > 5:
            pass
        else:
            if player_pos[1] < destination_pos[1]:
                player_pos[1] += 1
            elif player_pos[1] > destination_pos[1]:
                player_pos[1] -= 1

while True:
    for event in main.game.event.get():
        if event.type == main.game.QUIT:
            main.game.quit()
            sys.exit()
        
        if event.type == main.game.MOUSEBUTTONDOWN:
            mouse_pos = main.game.mouse.get_pos()
            destination_pos = get_grid_pos(mouse_pos)
    
    if destination_pos:
        if player_pos != destination_pos:
            move_towards_destination(player_pos, destination_pos)
            time.sleep(0.1)

    screen.fill(WHITE)
    draw_grid()
    draw_player(player_pos)
    main.game.display.flip()
    clock.tick(120)
