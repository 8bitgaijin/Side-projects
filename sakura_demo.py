# -*- coding: utf-8 -*-
"""
Falling Sakura Blossoms Simulation (Improved)
"""

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Sakura Blossoms")
clock = pygame.time.Clock()

# Colors: Pink shades for sakura petals
SAKURA_COLORS = [
    (255, 182, 193),  # Light Pink
    (255, 192, 203),  # Pink
    (255, 105, 180),  # Hot Pink
    (250, 128, 114),  # Salmon Pink
]

# Random color generator for sakura petals
def random_sakura_color():
    return random.choice(SAKURA_COLORS)

# Sakura Blossom Particle class
class SakuraBlossom:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(-200, -10)  # Start above the screen
        self.color = random_sakura_color()
        self.size = random.randint(10, 20)  # Blossom size
        self.speed = random.uniform(0.5, 1.5)  # Vertical speed
        self.sway = random.uniform(0.3, 1.0)  # Horizontal sway
        self.sway_direction = random.choice([-1, 1])  # Left or right
        self.settled = False

    def update(self):
        if not self.settled:
            # Vertical falling
            self.y += self.speed
            # Horizontal swaying
            sway_offset = math.sin(pygame.time.get_ticks() / 1000) * self.sway
            self.x += sway_offset * self.sway_direction

            # Keep within screen bounds
            self.x = max(0, min(WIDTH - 1, self.x))  # Clamp x to screen bounds

            # Check if blossom hits the ground
            if self.y >= HEIGHT - 1:
                self.y = HEIGHT - 1  # Snap to the ground
                self.settled = True  # Mark as settled

    def draw(self, surface):
        center_x, center_y = self.x, self.y
        petal_distance = self.size * 0.4  # Distance of petals from center (closer to center)
        petal_width = self.size * 0.7
        petal_height = self.size * 0.4

        for i in range(5):  # Draw five petals
            angle = i * (2 * math.pi / 5)  # Divide circle into 5 angles
            petal_x = center_x + math.cos(angle) * petal_distance
            petal_y = center_y + math.sin(angle) * petal_distance
            pygame.draw.ellipse(surface, self.color, (petal_x, petal_y, petal_width, petal_height))

# Particle system
particles = []
spawn_timer = 0  # Timer to space out blossom generation

# Main loop
running = True
while running:
    screen.fill((220, 220, 255))  # Light blue background for spring sky

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn new blossoms over time (spacing them out)
    spawn_timer += clock.get_time()
    if spawn_timer > 300:  # Spawn a new blossom every 300 ms
        if len(particles) < 500:  # Cap the total number of blossoms
            particles.append(SakuraBlossom())
        spawn_timer = 0  # Reset the timer

    # Update and draw particles
    for particle in particles:
        particle.update()
        particle.draw(screen)

    # Display FPS and particle count
    fps = clock.get_fps()
    font = pygame.font.Font(None, 36)
    fps_text = f"FPS: {fps:.2f}"
    particle_text = f"Particles: {len(particles)}"
    fps_surface = font.render(fps_text, True, (50, 50, 50))
    particle_surface = font.render(particle_text, True, (50, 50, 50))
    screen.blit(fps_surface, (10, 10))
    screen.blit(particle_surface, (10, 50))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
