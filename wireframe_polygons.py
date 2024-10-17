# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:33:47 2024

@author: Shane
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:40:06 2024

@author: Shane
"""

import pygame
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('3D Shapes in Pygame')

# Define vertices and edges for the cube
cube_vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Back face
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # Front face
]

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Back face edges
    (4, 5), (5, 6), (6, 7), (7, 4),  # Front face edges
    (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
]

# Define vertices and edges for a pyramid (square base)
pyramid_vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Base
    [0, 0, 1]  # Top point
]

pyramid_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Base edges
    (0, 4), (1, 4), (2, 4), (3, 4)   # Side edges connecting to the top
]

# Define vertices and edges for a tetrahedron
tetrahedron_vertices = [
    [1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]
]


tetrahedron_edges = [
    (0, 1), (0, 2), (0, 3),
    (1, 2), (1, 3), (2, 3)
]

# Projection function to convert 3D points to 2D
def project_3d_to_2d(point, screen_width, screen_height, fov=512, viewer_distance=10):
    """ Project a 3D point onto a 2D plane (the screen) using perspective projection. """
    factor = fov / (viewer_distance + point[2])
    x = point[0] * factor + screen_width / 2
    y = point[1] * factor + screen_height / 2
    return (int(x), int(y))

# Functions to rotate 3D points around the axes
def rotate_x(point, angle):
    """ Rotate a point around the X-axis. """
    y = point[1] * math.cos(angle) - point[2] * math.sin(angle)
    z = point[1] * math.sin(angle) + point[2] * math.cos(angle)
    return [point[0], y, z]

def rotate_y(point, angle):
    """ Rotate a point around the Y-axis. """
    x = point[2] * math.sin(angle) + point[0] * math.cos(angle)
    z = point[2] * math.cos(angle) - point[0] * math.sin(angle)
    return [x, point[1], z]

def rotate_z(point, angle):
    """ Rotate a point around the Z-axis. """
    x = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    y = point[0] * math.sin(angle) + point[1] * math.cos(angle)
    return [x, y, point[2]]

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0  # Initial angles for rotation
    current_shape = 'cube'  # Start with the cube

    while running:
        screen.fill((0, 0, 0))  # Clear the screen

        # Handle events (including exit on ESC key and shape selection with keys)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == KEYDOWN:
                if event.key == K_c:  # 'C' for Cube
                    current_shape = 'cube'
                elif event.key == K_p:  # 'P' for Pyramid
                    current_shape = 'pyramid'
                elif event.key == K_t:  # 'T' for Tetrahedron
                    current_shape = 'tetrahedron'

        # Choose vertices and edges based on the current shape
        if current_shape == 'cube':
            vertices = cube_vertices
            edges = cube_edges
        elif current_shape == 'pyramid':
            vertices = pyramid_vertices
            edges = pyramid_edges
        elif current_shape == 'tetrahedron':
            vertices = tetrahedron_vertices
            edges = tetrahedron_edges

        # Rotate the shape's vertices
        rotated_vertices = []
        for vertex in vertices:
            rotated = rotate_x(vertex, angle_x)
            rotated = rotate_y(rotated, angle_y)
            rotated = rotate_z(rotated, angle_z)
            rotated_vertices.append(rotated)

        # Project the 3D points to 2D and draw the edges of the shape
        projected_vertices = [project_3d_to_2d(vertex, screen_width, screen_height) for vertex in rotated_vertices]

        # Draw the edges of the shape
        for edge in edges:
            pygame.draw.line(screen, (255, 255, 255), projected_vertices[edge[0]], projected_vertices[edge[1]], 2)

        # Update the display
        pygame.display.flip()

        # Rotate the shape slightly
        angle_x += 0.01
        angle_y += 0.02
        angle_z += 0.015

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
