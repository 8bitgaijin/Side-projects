# -*- coding: utf-8 -*-
"""
Endless Snowfall Simulation (Simplified)
"""

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simplified Endless Snowfall")
clock = pygame.time.Clock()

# Colors: White to light blue
def random_snow_color():
    return (
        random.randint(200, 255),  # Red: High for white/light blue
        random.randint(200, 255),  # Green: High for white/light blue
        random.randint(255, 255)   # Blue: Max for light blue
    )

# Snowflake Particle class
class SnowflakeParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(-200, -10)  # Start above the screen
        self.color = random_snow_color()
        self.size = random.randint(5, 15)
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

            # Check if snowflake hits the ground
            if self.y >= HEIGHT - 1:
                self.y = HEIGHT - 1  # Snap to the ground
                self.settled = True  # Mark as settled

    def draw(self, surface):
        for i in range(6):  # Six lines radiating from center
            angle = i * math.pi / 3  # 60 degrees between each line
            end_x = self.x + math.cos(angle) * self.size
            end_y = self.y + math.sin(angle) * self.size
            pygame.draw.line(surface, self.color, (self.x, self.y), (end_x, end_y), 1)

# Particle system
particles = []

# Main loop
running = True
while running:
    screen.fill((10, 10, 40))  # Clear the screen with dark blue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn new snowflakes continuously
    particles.append(SnowflakeParticle())

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
