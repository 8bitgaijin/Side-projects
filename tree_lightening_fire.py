# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 14:49:47 2024

@author: Shane
"""

import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 800, 800
BACKGROUND_COLOR = (0, 0, 0)
TRUNK_COLOR = (139, 69, 19)  # Brown for trunk and branches
LEAF_COLOR = (34, 139, 34)   # Green for leaves
LIGHTNING_COLOR = (255, 255, 255)
BOLT_SEGMENTS = 10
BOLT_SPREAD = 50
BOLT_LIFETIME = 0.2  # Lifetime of each lightning bolt in seconds
PARTICLE_LIFETIME = 1.0  # Lifetime of fire particles in seconds
FIRE_COLORS = [(255, 69, 0), (255, 140, 0), (255, 165, 0)]  # Red, Orange, Yellow

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tree with Lightning and Fire")

# Particle class for fire simulation
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)  # Random horizontal velocity
        self.vy = random.uniform(-2, -1)  # Random upward velocity
        self.color = random.choice(FIRE_COLORS)
        self.size = random.randint(3, 7)
        self.lifetime = pygame.time.get_ticks()

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.size = max(0, self.size - 0.1)  # Gradually shrink the particle

    def is_alive(self):
        return pygame.time.get_ticks() - self.lifetime < PARTICLE_LIFETIME * 1000

    def draw(self, screen):
        if self.size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Function to draw a branch segment
def draw_branch(screen, start_pos, end_pos, thickness, color):
    pygame.draw.line(screen, color, start_pos, end_pos, thickness)

# Function to grow a static tree
def grow_tree(screen, start_x, start_y, max_depth, max_branches):
    branches = [(start_x, start_y, -90)]  # Starting trunk (x, y, angle - 90 degrees pointing up)
    branch_thickness = 10
    
    for depth in range(max_depth):
        new_branches = []
        
        for branch in branches:
            x, y, angle = branch
            branch_length = random.randint(10, 40)
            end_x = x + math.cos(math.radians(angle)) * branch_length
            end_y = y + math.sin(math.radians(angle)) * branch_length
            
            draw_branch(screen, (x, y), (end_x, end_y), branch_thickness, TRUNK_COLOR)
            
            num_new_branches = random.randint(1, max_branches)
            for _ in range(num_new_branches):
                new_angle = angle + random.randint(-40, 40)
                new_branches.append((end_x, end_y, new_angle))

            if depth == max_depth - 1:
                pygame.draw.circle(screen, LEAF_COLOR, (int(end_x), int(end_y)), 5)

        branches = new_branches
        branch_thickness = max(1, branch_thickness - 1)

# Function to draw lightning bolt and return collision point
def draw_lightning(screen, tree_surface, start_pos, end_pos):
    current_pos = start_pos
    start_color = (173, 216, 230)
    end_color = (255, 255, 255)
    collision_pos = None
    
    for i in range(BOLT_SEGMENTS):
        fraction = i / BOLT_SEGMENTS
        color = interpolate_color(start_color, end_color, fraction)
        
        next_x = current_pos[0] + random.randint(-BOLT_SPREAD, BOLT_SPREAD)
        next_y = current_pos[1] + (end_pos[1] - start_pos[1]) // BOLT_SEGMENTS
        next_pos = (next_x, next_y)
        
        pygame.draw.line(screen, color, current_pos, next_pos, 2)

        # Check pixel color at lightning bolt position to see if it hits the tree
        if 0 <= next_x < WIDTH and 0 <= next_y < HEIGHT:  # Ensure within screen bounds
            pixel_color = tree_surface.get_at((int(next_x), int(next_y)))
            if pixel_color[:3] == TRUNK_COLOR or pixel_color[:3] == LEAF_COLOR:  # Hit tree
                collision_pos = (next_x, next_y)  # Store the collision position
        
        current_pos = next_pos
    
    pygame.draw.line(screen, end_color, current_pos, end_pos, 2)
    
    return collision_pos

# Function to interpolate color
def interpolate_color(start_color, end_color, fraction):
    return (
        start_color[0] + (end_color[0] - start_color[0]) * fraction,
        start_color[1] + (end_color[1] - start_color[1]) * fraction,
        start_color[2] + (end_color[2] - start_color[2]) * fraction,
    )

# Main loop
clock = pygame.time.Clock()
running = True
lightning_bolts = []
particles = []
tree_top = HEIGHT // 2  # The top of the tree

# Create a separate surface to draw the static tree
tree_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
grow_tree(tree_surface, WIDTH // 2, HEIGHT, max_depth=10, max_branches=2)  # Draw the tree onto this surface

# Draw the tree once on the tree surface
screen.blit(tree_surface, (0, 0))
pygame.display.flip()

while running:
    screen.fill(BACKGROUND_COLOR)
    screen.blit(tree_surface, (0, 0))  # Blit the pre-drawn static tree onto the screen
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            end_pos = (mouse_x, HEIGHT)
            lightning_bolts.append(((mouse_x, mouse_y), end_pos, pygame.time.get_ticks()))
            print(f"Mouse clicked at ({mouse_x}, {mouse_y}), lightning target at {end_pos}")

            # Draw lightning and get collision point
            collision_pos = draw_lightning(screen, tree_surface, (mouse_x, mouse_y), end_pos)

            # Fire starts at collision point or ground
            if collision_pos:
                fire_start_x, fire_start_y = collision_pos  # Fire from where lightning hit the tree
            else:
                fire_start_x, fire_start_y = mouse_x, HEIGHT  # Fire from ground if no tree is hit

            # Generate fire particles at strike point
            for _ in range(20):
                particles.append(Particle(fire_start_x, fire_start_y))

    current_time = pygame.time.get_ticks()
    lightning_bolts = [bolt for bolt in lightning_bolts if (current_time - bolt[2]) < (BOLT_LIFETIME * 1000)]

    # Draw the active lightning bolts
    for bolt in lightning_bolts:
        draw_lightning(screen, tree_surface, bolt[0], bolt[1])

    # Update and draw particles (fire effect)
    particles = [p for p in particles if p.is_alive()]
    for particle in particles:
        particle.update()
        particle.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
