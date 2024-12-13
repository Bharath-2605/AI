import pygame
import random
pygame.init()
WIDTH, HEIGHT = 600, 600
BACKGROUND_COLOR = (30, 30, 30)
GRID_LINE_COLOR = (200, 200, 200)
DUST_COLOR = (223, 255, 0)
VACUUM_COLOR = (92, 184, 92)
def create_grid(rows, num_dust):
    grid = [[False for _ in range(rows)] for _ in range(rows)]
    all_positions = [(i, j) for i in range(rows) for j in range(rows)]
    dust_positions = random.sample(all_positions, num_dust)
    for pos in dust_positions:
        grid[pos[0]][pos[1]] = True
    return grid
def draw_grid(screen, grid, vacuum_pos):
    tile_size = WIDTH // len(grid)
    for i in range(len(grid)):
        for j in range(len(grid)):
            x, y = j * tile_size, i * tile_size
            pygame.draw.rect(screen, GRID_LINE_COLOR, (x, y, tile_size, tile_size), 1)
            if grid[i][j]:
                pygame.draw.circle(screen, DUST_COLOR, (x + tile_size // 2, y + tile_size // 2), tile_size // 6)
            if (i, j) == vacuum_pos:
                pygame.draw.rect(screen, VACUUM_COLOR, (x + tile_size // 4, y + tile_size // 4, tile_size // 2, tile_size // 2))
def generate_path(rows, start_pos):
    path = []
    start_x, start_y = start_pos
    for i in range(rows):
        if i % 2 == 0:
            for j in range(rows):
                path.append((j, i))
        else:
            for j in range(rows - 1, -1, -1):
                path.append((j, i))
    start_index = path.index(start_pos)
    path = path[start_index:] + path[:start_index]
    path.append(start_pos)
    return path
def linear_to_grid(index, rows):
    """Convert a linear index to grid coordinates."""
    return index // rows, index % rows
def main():
    rows = int(input("Enter the number of tiles per row/column: "))
    num_dust = int(input("Enter the number of dust tiles to generate: "))
    start_index = int(input("Enter the starting position (0-indexed): "))
    if start_index >= rows * rows or start_index < 0:
        print("Invalid starting position. Must be within the grid size.")
        return
    if num_dust > rows * rows:
        print("Too many dust tiles! The number of dust tiles cannot exceed the total number of tiles.")
        return
    start_pos = linear_to_grid(start_index, rows)
    grid = create_grid(rows, num_dust)
    path = generate_path(rows, start_pos)
    vacuum_pos = start_pos
    screen.fill(BACKGROUND_COLOR)
    clock = pygame.time.Clock()
    running = True
    path_index = 0
    while running:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if path_index < len(path):
            vacuum_pos = path[path_index]
            if grid[vacuum_pos[0]][vacuum_pos[1]]:
                grid[vacuum_pos[0]][vacuum_pos[1]] = False
            path_index += 1
        draw_grid(screen, grid, vacuum_pos)
        pygame.display.flip()
        clock.tick(2)
    pygame.quit()
if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Vacuum Cleaner Simulation")
    main()
