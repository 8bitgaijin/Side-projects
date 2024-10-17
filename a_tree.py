import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 800, 800
BACKGROUND_COLOR = (0, 0, 0)
TRUNK_COLOR = (139, 69, 19)  # Brown for trunk and branches
LEAF_COLOR = (34, 139, 34)   # Green for leaves

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Growth Tree")

# Function to draw a branch segment
def draw_branch(screen, start_pos, end_pos, thickness, color):
    pygame.draw.line(screen, color, start_pos, end_pos, thickness)

# Function to grow a tree
def grow_tree(screen, start_x, start_y, max_depth, max_branches):
    branches = [(start_x, start_y, -90)]  # Starting trunk (x, y, angle - 90 degrees pointing up)
    branch_thickness = 10  # Start thickness for the trunk
    
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

            # At the end of depth, we add leaves
            if depth == max_depth - 1:
                pygame.draw.circle(screen, LEAF_COLOR, (int(end_x), int(end_y)), 5)  # Leaves at the tips

        # Update for next depth
        branches = new_branches
        branch_thickness = max(1, branch_thickness - 1)  # Decrease thickness with each level

# Main loop
def main():
    screen.fill(BACKGROUND_COLOR)
    
    # Start growing tree from the exact bottom center
    grow_tree(screen, WIDTH // 2, HEIGHT, max_depth=10, max_branches=2)
    
    pygame.display.flip()  # Display the tree

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
