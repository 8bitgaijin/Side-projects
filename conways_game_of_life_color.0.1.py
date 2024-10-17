import pygame
import random

# Constants
GRID_SIZE = 10  # Size of each cell
FPS = 100

# Colors (Monochromatic Blue, no darkest shades)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE_1 = (200, 220, 255)
LIGHT_BLUE_2 = (150, 190, 255)
LIGHT_BLUE_3 = (100, 160, 255)
LIGHT_BLUE_4 = (50, 130, 255)
BLUE_1 = (0, 100, 255)
BLUE_2 = (0, 80, 200)
BLUE_3 = (0, 60, 150)

# Initialize pygame and set up full-screen with automatic resolution
def init():
    pygame.init()
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h  # Get current screen resolution
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)  # Fullscreen with current resolution
    pygame.display.set_caption('Conway\'s Game of Life with Monochromatic Blue Colors')
    clock = pygame.time.Clock()
    return screen, clock, screen_width, screen_height

# Initialize a random grid of alive (1) and dead (0) cells, with a generation counter
def init_grid(cols, rows):
    return [[(random.choice([0, 1]), 0) for _ in range(cols)] for _ in range(rows)]

# Count the number of live neighbors for a given cell
def count_neighbors(grid, row, col, rows, cols):
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r = (row + i) % rows
            c = (col + j) % cols
            neighbors += grid[r][c][0]  # Only count alive status
    return neighbors

# Update the grid based on Conway's Game of Life rules, with generation tracking
def update_grid(grid, rows, cols, clicked_cells):
    new_grid = [[(0, 0) for _ in range(cols)] for _ in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            alive, generations = grid[row][col]
            neighbors = count_neighbors(grid, row, col, rows, cols)
            
            # If the cell was clicked, keep it alive
            if (row, col) in clicked_cells:
                new_grid[row][col] = (1, generations + 1)
                continue
            
            # Normal Conway's Game of Life rules
            if alive == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = (0, 0)  # Death by overcrowding or loneliness
                else:
                    new_grid[row][col] = (1, min(generations + 1, 6))  # Cap generations at 6
            else:
                if neighbors == 3:
                    new_grid[row][col] = (1, 1)  # Birth of a new cell, starting generation count
    return new_grid

# Get the color for a cell based on the number of generations it has survived (Monochromatic Blue)
def get_cell_color(generations):
    if generations == 0:
        return WHITE
    elif generations == 1:
        return LIGHT_BLUE_1
    elif generations == 2:
        return LIGHT_BLUE_2
    elif generations == 3:
        return LIGHT_BLUE_3
    elif generations == 4:
        return LIGHT_BLUE_4
    elif generations == 5:
        return BLUE_1
    else:
        return BLUE_2  # For generation 6 and beyond (no darker blues)

# Draw the grid on the screen
def draw_grid(screen, grid, rows, cols, grid_size):
    for row in range(rows):
        for col in range(cols):
            alive, generations = grid[row][col]
            color = get_cell_color(generations) if alive == 1 else BLACK
            pygame.draw.rect(screen, color, (col * grid_size, row * grid_size, grid_size, grid_size))
    
    pygame.display.flip()

# Handle spawning new live cells with mouse clicks
def handle_mouse_click(grid, screen_width, screen_height, grid_size, clicked_cells):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    col = mouse_x // grid_size
    row = mouse_y // grid_size
    if 0 <= col < screen_width // grid_size and 0 <= row < screen_height // grid_size:
        clicked_cells.add((row, col))  # Add clicked cell to the set of manually spawned cells
        grid[row][col] = (1, 1)  # Spawn the cell with generation 1
    return grid

# Main game loop with ESC key exit and full-screen auto-adjust
def main_loop(screen, clock, screen_width, screen_height):
    cols = screen_width // GRID_SIZE
    rows = screen_height // GRID_SIZE
    grid = init_grid(cols, rows)  # Initialize the grid with dynamic row/column counts
    clicked_cells = set()  # Store cells that have been manually spawned by the player
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Exit on ESC key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                grid = handle_mouse_click(grid, screen_width, screen_height, GRID_SIZE, clicked_cells)  # Handle clicks to spawn cells

        # Update the grid
        grid = update_grid(grid, rows, cols, clicked_cells)

        # Draw the updated grid
        draw_grid(screen, grid, rows, cols, GRID_SIZE)

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    screen, clock, screen_width, screen_height = init()
    main_loop(screen, clock, screen_width, screen_height)
