import pygame
import random
pygame.init()
WIDTH, HEIGHT = 600, 600
BACKGROUND_COLOR = (30, 30, 30)
GRID_LINE_COLOR = (200, 200, 200)
DUST_COLOR = (223, 255, 0)  # Chartreuse Yellow
VACUUM_COLOR = (92, 184, 92)  # Brick Grenadier

# Function to create grid based on user-defined rows
def create_grid(rows):
    return [[random.choice([True, False]) for _ in range(rows)] for _ in range(rows)]

# Function to draw the board and elements
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

# Function for vacuum cleaner movement along a zigzag path starting from a given position
def generate_path(rows, start_pos):
    path = []
    start_x, start_y = start_pos

    # Create a zigzag path starting from the given position
    for i in range(rows):
        if i % 2 == 0:
            for j in range(rows):
                path.append((j, i))
        else:
            for j in range(rows - 1, -1, -1):
                path.append((j, i))

    # Ensure the path starts from the user-defined start position
    start_index = path.index(start_pos)
    path = path[start_index:] + path[:start_index]  # Reorder the path to start at the given position

    return path

# Main function
def main():
    # User input
    rows = int(input("Enter the number of tiles per row/column: "))
    start_x = int(input("Enter the starting x position (0-indexed): "))
    start_y = int(input("Enter the starting y position (0-indexed): "))

    # Ensure starting position is valid
    if start_x >= rows or start_y >= rows or start_x < 0 or start_y < 0:
        print("Invalid starting position. Must be within the grid size.")
        return

    start_pos = (start_x, start_y)
    grid = create_grid(rows)

    # Generate a zigzag path covering all tiles and starting from the start position
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

            # Clear dust if present at the current vacuum position
            if grid[vacuum_pos[0]][vacuum_pos[1]]:
                grid[vacuum_pos[0]][vacuum_pos[1]] = False  # Clear dust only if present

            path_index += 1

        draw_grid(screen, grid, vacuum_pos)
        pygame.display.flip()
        clock.tick(2)  # Adjust speed of vacuum movement

    pygame.quit()

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Vacuum Cleaner Simulation")
    main()
