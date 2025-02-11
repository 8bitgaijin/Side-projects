# -*- coding: utf-8 -*-
"""
Endless Falling Leaves Simulation with 10 Colors
"""

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Falling Leaves")
clock = pygame.time.Clock()

# Colors: Brown, Red, and Orange with intermediate shades
LEAF_COLORS = [
    (139, 69, 19),   # Brown
    (160, 82, 45),   # Light Brown
    (205, 92, 92),   # Rosy Brown
    (255, 69, 0),    # Red
    (255, 99, 71),   # Tomato
    (255, 140, 0),   # Dark Orange
    (255, 165, 0),   # Orange
    (255, 185, 15),  # Light Orange
    (218, 165, 32),  # Goldenrod
    (184, 134, 11)   # Dark Goldenrod
]

# Random color generator for leaves
def random_leaf_color():
    return random.choice(LEAF_COLORS)

# Leaf Particle class
class LeafParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(-200, -10)  # Start above the screen
        self.color = random_leaf_color()
        self.width = random.randint(10, 20)  # Width of the oval
        self.height = random.randint(5, 10)  # Height of the oval
        self.speed = random.uniform(1, 2)  # Vertical speed
        self.sway = random.uniform(0.5, 1.5)  # Horizontal sway
        self.sway_direction = random.choice([-1, 1])  # Left or right
        self.settled = False

    def update(self):
        if not self.settled:
            # Vertical falling
            self.y += self.speed
            # Horizontal swaying
            sway_offset = math.sin(pygame.time.get_ticks() / 500) * self.sway
            self.x += sway_offset * self.sway_direction

            # Keep within screen bounds
            self.x = max(0, min(WIDTH - 1, self.x))  # Clamp x to screen bounds

            # Check if leaf hits the ground
            if self.y >= HEIGHT - 1:
                self.y = HEIGHT - 1  # Snap to the ground
                self.settled = True  # Mark as settled

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, (self.x, self.y, self.width, self.height))

# Particle system
particles = []

# Main loop
running = True
while running:
    screen.fill((30, 15, 10))  # Dark earthy background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn new leaves continuously
    particles.append(LeafParticle())

    # Update and draw particles
    for particle in particles:
        particle.update()
        particle.draw(screen)

    # Display FPS and particle count
    fps = clock.get_fps()
    font = pygame.font.Font(None, 36)
    fps_text = f"FPS: {fps:.2f}"
    particle_text = f"Particles: {len(particles)}"
    fps_surface = font.render(fps_text, True, (255, 255, 255))
    particle_surface = font.render(particle_text, True, (255, 255, 255))
    screen.blit(fps_surface, (10, 10))
    screen.blit(particle_surface, (10, 50))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
