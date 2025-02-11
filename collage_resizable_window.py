# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:20:34 2024

@author: Shane
"""

import pygame
import os
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Initial screen dimensions (can be adjusted)
initial_width = 800
initial_height = 600

# Create a resizable window
screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
pygame.display.set_caption('Photo Collage')

# Variables for controlling draw speed (milliseconds between images) and max tilt angle
draw_speed = 500  # Control how fast each image is drawn (in milliseconds)
max_angle = 20    # Control the maximum tilt angle (in degrees)

# Function to load, scale, and tilt image randomly
def load_scale_and_tilt_random_image():
    valid_extensions = ['.png', '.jpg', '.jpeg']
    image_files = [f for f in os.listdir('.') if os.path.isfile(f) and os.path.splitext(f)[1].lower() in valid_extensions]

    if not image_files:
        return None  # Return None if no valid images are found

    random_image_path = random.choice(image_files)
    image = pygame.image.load(random_image_path).convert_alpha()  # Ensure the image retains transparency
    image_width, image_height = image.get_size()

    # Ensure the image does not exceed the screen dimensions
    max_scale_factor = min(screen.get_width() / image_width, screen.get_height() / image_height)

    # Pick a random scale factor between 0.2 and the maximum scale factor
    scale_factor = random.uniform(0.2, min(0.8, max_scale_factor))
    new_width = int(image_width * scale_factor)
    new_height = int(image_height * scale_factor)

    # Scale the image down to fit within the random size
    scaled_image = pygame.transform.scale(image, (new_width, new_height))

    # Rotate the image by a random angle between -max_angle and +max_angle, excluding 0 degrees (to avoid straight up/down)
    tilt_angle = random.choice([random.uniform(-max_angle, -5), random.uniform(5, max_angle)])
    tilted_image = pygame.transform.rotate(scaled_image, tilt_angle)

    return tilted_image

# Function to draw image at a random position
def draw_image_at_random_position(image):
    if image is None:
        return

    image_width, image_height = image.get_size()

    # Make sure the random position keeps the image fully within the screen
    x_pos = random.randint(0, max(0, screen.get_width() - image_width))
    y_pos = random.randint(0, max(0, screen.get_height() - image_height))

    screen.blit(image, (x_pos, y_pos))


# Function to handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close the window button
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Escape key to quit
            return False
        if event.type == pygame.VIDEORESIZE:  # Handle window resizing
            global screen
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    return True

# Main loop for photo collage
def photo_collage():
    screen.fill((0, 0, 0))  # Start with a black screen
    running = True

    while running:
        # Handle the events
        if not handle_events():
            break

        # Load, scale, and tilt a random image
        random_image = load_scale_and_tilt_random_image()

        # Draw the image at a random position on the screen
        draw_image_at_random_position(random_image)

        # Update the display but do not clear the screen, letting the images overlap
        pygame.display.flip()

        # Delay based on the draw speed
        pygame.time.delay(draw_speed)

    pygame.quit()

if __name__ == "__main__":
    photo_collage()
