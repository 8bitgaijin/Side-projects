# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 12:39:57 2024

@author: Shane
"""

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Particle Benchmark")
clock = pygame.time.Clock()

# Particle effects list
particle_effects = ["pixel", "line", "circle", "arc", "polygon", "snowflake"]

# Colors
WHITE = (255, 255, 255)
COLORS = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 0), (255, 0, 255)]

# Particle class
class Particle:
    def __init__(self, effect_type):
        self.effect_type = effect_type
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.color = random.choice(COLORS)
        self.size = random.randint(5, 15)  # Snowflake size is slightly larger
        self.angle = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(1, 5)
        self.life = random.randint(30, 100)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1

    def draw(self, surface):
        if self.effect_type == "pixel":
            pygame.draw.line(surface, self.color, (self.x, self.y), (self.x, self.y))  # Single pixel
        elif self.effect_type == "line":
            end_x = self.x + math.cos(self.angle) * self.size
            end_y = self.y + math.sin(self.angle) * self.size
            pygame.draw.line(surface, self.color, (self.x, self.y), (end_x, end_y), 1)
        elif self.effect_type == "circle":
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size, 0)
        elif self.effect_type == "arc":
            rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
            start_angle = self.angle
            end_angle = self.angle + math.pi / 2
            pygame.draw.arc(surface, self.color, rect, start_angle, end_angle, 1)
        elif self.effect_type == "polygon":
            points = [
                (self.x, self.y),
                (self.x + random.randint(-10, 10), self.y + random.randint(-10, 10)),
                (self.x + random.randint(-10, 10), self.y + random.randint(-10, 10))
            ]
            pygame.draw.polygon(surface, self.color, points)
        elif self.effect_type == "snowflake":  # New snowflake particle
            for i in range(6):  # Six lines radiating from center
                angle = i * math.pi / 3  # 60 degrees between each line
                end_x = self.x + math.cos(angle) * self.size
                end_y = self.y + math.sin(angle) * self.size
                pygame.draw.line(surface, self.color, (self.x, self.y), (end_x, end_y), 1)

# Particle system
particles = []
current_effect = 0
particle_count = 10  # Start with a small number of particles
fullscreen = False  # Track fullscreen state

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Cycle through effects
                current_effect = (current_effect + 1) % len(particle_effects)
            if event.key == pygame.K_RETURN:  # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    WIDTH, HEIGHT = screen.get_size()
                else:
                    screen = pygame.display.set_mode((1024, 768))
                    WIDTH, HEIGHT = 1024, 768

    # Spawn particles dynamically based on particle count
    for _ in range(particle_count - len(particles)):
        particles.append(Particle(particle_effects[current_effect]))

    # Update and draw particles
    for particle in particles[:]:
        particle.update()
        particle.draw(screen)
        if particle.life <= 0:
            particles.remove(particle)

    # Adjust particle count dynamically based on FPS
    fps = clock.get_fps()
    if fps >= 60:
        particle_count += 100  # Increase particles if FPS is stable at 60+
    elif fps < 50:
        particle_count = max(1, particle_count - 10)  # Decrease particles if FPS drops below 50

    # Display FPS and particle count
    font = pygame.font.Font(None, 36)
    fps_text = f"FPS: {fps:.2f}"
    fps_surface = font.render(fps_text, True, WHITE)
    screen.blit(fps_surface, (10, 10))

    particle_text = f"Particles: {particle_count}"
    particle_surface = font.render(particle_text, True, WHITE)
    screen.blit(particle_surface, (10, 50))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
