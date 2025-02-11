# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:00:59 2024

@author: Shane
"""

import pygame
import math
import colorsys  # Import colorsys for HSV to RGB conversion
from pygame.locals import *
import pyttsx3  # Import TTS engine
import threading  # For running TTS in a separate thread
import random  # To randomize positions of "Clicked"

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('3D Cube Mouse Pointer')

# Define font for FPS and clicked text display
font = pygame.font.SysFont('Arial', 18)
clicked_font = pygame.font.SysFont('Arial', 36)

# Define vertices and edges for the cube
cube_vertices = [
    [-1, -1, -1],  # 0: Back-bottom-left
    [1, -1, -1],   # 1: Back-bottom-right
    [1, 1, -1],    # 2: Back-top-right
    [-1, 1, -1],   # 3: Back-top-left
    [-1, -1, 1],   # 4: Front-bottom-left
    [1, -1, 1],    # 5: Front-bottom-right
    [1, 1, 1],     # 6: Front-top-right
    [-1, 1, 1]     # 7: Front-top-left
]

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Back face edges
    (4, 5), (5, 6), (6, 7), (7, 4),  # Front face edges
    (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
]

# Projection function to convert 3D points to 2D
def project_3d_to_2d(point, center_x, center_y, fov=512, viewer_distance=10):
    """Project a 3D point onto a 2D plane (the screen) using perspective projection."""
    factor = fov / (viewer_distance + point[2])
    x = point[0] * factor + center_x
    y = -point[1] * factor + center_y  # Invert y-axis to match Pygame's coordinate system
    return (int(x), int(y))

# Functions to rotate 3D points around the axes
def rotate_x(point, angle):
    """Rotate a point around the X-axis."""
    y = point[1] * math.cos(angle) - point[2] * math.sin(angle)
    z = point[1] * math.sin(angle) + point[2] * math.cos(angle)
    return [point[0], y, z]

def rotate_y(point, angle):
    """Rotate a point around the Y-axis."""
    x = point[2] * math.sin(angle) + point[0] * math.cos(angle)
    z = point[2] * math.cos(angle) - point[0] * math.sin(angle)
    return [x, point[1], z]

def rotate_z(point, angle):
    """Rotate a point around the Z-axis."""
    x = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    y = point[0] * math.sin(angle) + point[1] * math.cos(angle)
    return [x, y, point[2]]

# Function to read "Clicked" using a new TTS engine instance in a separate thread
def read_tts():
    engine = pyttsx3.init()  # Create a new TTS engine instance for each thread
    engine.say("Clicked")
    engine.runAndWait()

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0  # Initial angles for rotation

    hue_cube = 0.0  # Initial hue value for cube
    hue_fps = 0.5   # Initial hue value for FPS (offset from cube)

    # Variables to store multiple "Clicked" events
    click_events = []

    while running:
        screen.fill((0, 0, 0))  # Clear the screen

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == MOUSEBUTTONDOWN:
                # Spawn a new "Clicked" event with random position and current time
                random_x = random.randint(50, screen_width - 50)
                random_y = random.randint(50, screen_height - 50)
                click_time = pygame.time.get_ticks()
                
                # Add the new event to the list
                click_events.append((random_x, random_y, click_time))

                # Create a new thread to handle TTS and avoid blocking the main loop
                tts_thread = threading.Thread(target=read_tts)
                tts_thread.start()

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Rotate the cube's vertices
        rotated_vertices = []
        for vertex in cube_vertices:
            rotated = rotate_x(vertex, angle_x)
            rotated = rotate_y(rotated, angle_y)
            rotated = rotate_z(rotated, angle_z)
            rotated_vertices.append(rotated)

        # Project the 3D points to 2D at the mouse's position
        projected_vertices = [
            project_3d_to_2d(vertex, mouse_x, mouse_y) for vertex in rotated_vertices
        ]

        # Update the hue values to cycle through colors
        hue_cube += 0.00833  # Adjust the speed of color cycling (approx. every 2 seconds)
        hue_fps += 0.00833   # Same cycle speed for FPS, but with an offset

        if hue_cube > 1.0:
            hue_cube -= 1.0  # Loop the hue value for the cube

        if hue_fps > 1.0:
            hue_fps -= 1.0   # Loop the hue value for the FPS

        # Convert HSV to RGB for cube edges
        r_cube, g_cube, b_cube = colorsys.hsv_to_rgb(hue_cube, 1.0, 1.0)
        edge_color = (int(r_cube * 255), int(g_cube * 255), int(b_cube * 255))

        # Convert HSV to RGB for FPS text (offset color)
        r_fps, g_fps, b_fps = colorsys.hsv_to_rgb(hue_fps, 1.0, 1.0)
        fps_color = (int(r_fps * 255), int(g_fps * 255), int(b_fps * 255))

        # Draw the edges of the cube with the dynamic color
        for edge in cube_edges:
            pygame.draw.line(
                screen, edge_color, projected_vertices[edge[0]], projected_vertices[edge[1]], 2
            )

        # Rotate the cube slightly
        angle_x += 0.01
        angle_y += 0.02
        angle_z += 0.015

        # Calculate FPS and render it to the screen with cycling color
        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {int(fps)}", True, fps_color)
        screen.blit(fps_text, (10, 10))

        # Iterate over the list of click events and render each "Clicked" text
        current_time = pygame.time.get_ticks()
        for (x, y, start_time) in click_events[:]:
            if current_time - start_time < 1000:  # Display each "Clicked" for 1 second
                click_text = clicked_font.render("Clicked", True, pygame.Color('white'))
                text_rect = click_text.get_rect(center=(x, y))
                screen.blit(click_text, text_rect)
            else:
                # Remove the event once it's been shown for 1 second
                click_events.remove((x, y, start_time))

        # Update the display
        pygame.display.flip()

        # No FPS cap, just track the time
        clock.tick()

    pygame.quit()

if __name__ == "__main__":
    main()
