# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:00:59 2024

@author: Shane
"""

import pygame
import math
import colorsys  # Import colorsys for HSV to RGB conversion
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('3D Cube Mouse Pointer')

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

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0  # Initial angles for rotation

    hue = 0.0  # Initial hue value

    while running:
        screen.fill((0, 0, 0))  # Clear the screen

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

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

        # Update the hue value to cycle through colors
        hue += 0.00833  # Adjust the speed of color cycling (approx. every 2 seconds)
        if hue > 1.0:
            hue -= 1.0  # Loop the hue value

        # Convert HSV to RGB with full saturation and value for bright colors
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        edge_color = (int(r * 255), int(g * 255), int(b * 255))

        # Draw the edges of the cube with the dynamic color
        for edge in cube_edges:
            pygame.draw.line(
                screen, edge_color, projected_vertices[edge[0]], projected_vertices[edge[1]], 2
            )

        # Rotate the cube slightly
        angle_x += 0.01
        angle_y += 0.02
        angle_z += 0.015

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
