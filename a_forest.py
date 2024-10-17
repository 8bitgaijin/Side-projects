import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 800, 800
BACKGROUND_COLOR = (0, 0, 0)
TRUNK_COLOR = (139, 69, 19)  # Brown for trunk and branches
LEAF_COLOR = (34, 139, 34)   # Green for leaves
MAX_TREES = 100  # Total number of trees
MAX_ROWS = 3    # Total number of rows
START_HEIGHT = HEIGHT * 0.5  # Start the rows from 50% of the screen

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recursive Forest")

# Function to draw a branch segment
def draw_branch(screen, start_pos, end_pos, thickness, color):
    pygame.draw.line(screen, color, start_pos, end_pos, thickness)

# Function to grow a single tree
def grow_tree(screen, start_x, start_y, max_depth, max_branches, branch_thickness):
    branches = [(start_x, start_y, -90)]  # Starting trunk (x, y, angle - 90 degrees pointing up)

    for depth in range(max_depth):
        new_branches = []

        for branch in branches:
            x, y, angle = branch
            branch_length = random.randint(10, 40)  # Random length for variety

            # Calculate new branch endpoint
            end_x = x + math.cos(math.radians(angle)) * branch_length
            end_y = y + math.sin(math.radians(angle)) * branch_length

            # Draw the branch
            draw_branch(screen, (x, y), (end_x, end_y), branch_thickness, TRUNK_COLOR)

            # Randomly decide how many branches to grow from this segment
            num_new_branches = random.randint(1, max_branches)

            for _ in range(num_new_branches):
                new_angle = angle + random.randint(-40, 40)  # Random angle variation
                new_branches.append((end_x, end_y, new_angle))  # Append new branches

            # Add leaves at the end of the branch at the max depth
            if depth == max_depth - 1:
                pygame.draw.circle(screen, LEAF_COLOR, (int(end_x), int(end_y)), 5)  # Leaves at the tips

        # Update branches for the next depth level
        branches = new_branches
        branch_thickness = max(1, branch_thickness - 1)  # Decrease thickness with each level

# Function to calculate the number of trees per row based on proximity to the horizon
def calculate_tree_distribution(max_trees, max_rows):
    tree_distribution = []
    total_weight = sum(range(1, max_rows + 1))  # Weighting based on row proximity to horizon
    for row in range(1, max_rows + 1):
        row_weight = row / total_weight
        row_trees = int(max_trees * row_weight)
        tree_distribution.append(row_trees)
    return tree_distribution

# Function to grow a forest with trees in rows
def grow_forest(screen, max_trees, max_rows):
    tree_distribution = calculate_tree_distribution(max_trees, max_rows)
    
    row_height_increment = (HEIGHT * 0.6) / max_rows  # Distribute rows from 50% to just below the screen

    for row in range(max_rows):
        row_trees = tree_distribution[row]
        row_height = START_HEIGHT + row * row_height_increment

        for _ in range(row_trees):
            # Randomly position trees across the row's width
            tree_x = random.randint(20, WIDTH - 20)

            # Adjust complexity of trees for each row (lower rows are taller and more intricate)
            max_depth = random.randint(3 + row, 6 + row)  # Deeper trees for lower rows
            max_branches = random.randint(2, 5 + row)  # More branches for lower rows
            branch_thickness = random.randint(2 + row, 5 + row)

            # Grow a single tree in the current row
            grow_tree(screen, tree_x, row_height, max_depth, max_branches, branch_thickness)

# Main loop
def main():
    screen.fill(BACKGROUND_COLOR)

    # Grow the forest with recursive rows
    grow_forest(screen, MAX_TREES, MAX_ROWS)

    pygame.display.flip()  # Display the forest

    # Event loop to exit on ESC
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
