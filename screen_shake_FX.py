# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 12:39:02 2024

@author: Shane
"""

import pygame
import random

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create a dummy surface
scene = pygame.Surface((WIDTH, HEIGHT))
scene.fill((50, 50, 100))  # Background color

# Shake parameters
shake_intensity = 10  # Max pixel movement
shake_duration = 0.5  # Seconds
shake_timer = 0

running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Trigger shake
                shake_timer = shake_duration

    # Drawing the scene
    scene.fill((50, 50, 100))  # Refill the dummy scene
    pygame.draw.circle(scene, (200, 50, 50), (WIDTH // 2, HEIGHT // 2), 50)

    # Apply shake effect
    if shake_timer > 0:
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        shake_timer -= dt
    else:
        offset_x, offset_y = 0, 0

    # Blit the scene with the offset
    screen.fill((0, 0, 0))  # Clear screen
    screen.blit(scene, (offset_x, offset_y))
    pygame.display.flip()

pygame.quit()
