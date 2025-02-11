# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 13:20:30 2024

@author: Shane
"""

import pygame
import math
import colorsys  # For HSV to RGB conversion
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('3D Icosahedron Painter')

# Icosahedron vertices and edges
t = (1 + math.sqrt(5)) / 2  # Golden ratio
ico_vertices = [
    [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],  # Around the X-axis
    [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],  # Around the Y-axis
    [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]   # Around the Z-axis
]

# Corrected edges for a proper icosahedron shape
ico_edges = [
    # Connect each vertex to the 5 nearest vertices
    (0, 1), (0, 5), (0, 7), (0, 10), (0, 11),
    (1, 5), (1, 7), (1, 8), (1, 9), 
    (2, 3), (2, 4), (2, 6), (2, 10), (2, 11),
    (3, 4), (3, 6), (3, 8), (3, 9), 
    (4, 5), (4, 9), (4, 11),
    (5, 9), (5, 11),
    (6, 7), (6, 10), (6, 8),
    (7, 10), (7, 8),
    (8, 9), 
    # (9, 11), 
    (10, 11)
]

# Projection function to convert 3D points to 2D
def project_3d_to_2d(point, center_x, center_y, fov=512, viewer_distance=10):
    factor = fov / (viewer_distance + point[2])
    x = point[0] * factor + center_x
    y = -point[1] * factor + center_y  # Invert y-axis to match Pygame's coordinate system
    return (int(x), int(y))

# Functions to rotate 3D points around the axes
def rotate_x(point, angle):
    y = point[1] * math.cos(angle) - point[2] * math.sin(angle)
    z = point[1] * math.sin(angle) + point[2] * math.cos(angle)
    return [point[0], y, z]

def rotate_y(point, angle):
    x = point[2] * math.sin(angle) + point[0] * math.cos(angle)
    z = point[2] * math.cos(angle) - point[0] * math.sin(angle)
    return [x, point[1], z]

def rotate_z(point, angle):
    x = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    y = point[0] * math.sin(angle) + point[1] * math.cos(angle)
    return [x, y, point[2]]

# Define the Icosahedron class
class Icosahedron:
    def __init__(self, position):
        self.position = position  # (center_x, center_y)
        self.vertices = ico_vertices
        self.edges = ico_edges
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.hue = 0.0  # Initial hue for color cycling

    def update(self):
        self.angle_x += 0.01
        self.angle_y += 0.02
        self.angle_z += 0.015

        # Update the hue value to cycle through colors
        self.hue += 0.00833  # Adjust the speed of color cycling
        if self.hue > 1.0:
            self.hue -= 1.0

    def draw(self, screen):
        # Rotate the Icosahedron's vertices in 3D space
        rotated_vertices = []
        for vertex in self.vertices:
            rotated = rotate_x(vertex, self.angle_x)
            rotated = rotate_y(rotated, self.angle_y)
            rotated = rotate_z(rotated, self.angle_z)
            rotated_vertices.append(rotated)

        # Project the 3D points to 2D
        projected_vertices = [
            project_3d_to_2d(vertex, self.position[0], self.position[1])
            for vertex in rotated_vertices
        ]

        # Convert HSV to RGB for color cycling
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        edge_color = (int(r * 255), int(g * 255), int(b * 255))

        # Draw the edges of the Icosahedron
        for edge in self.edges:
            pygame.draw.line(
                screen, edge_color, projected_vertices[edge[0]], projected_vertices[edge[1]], 2
            )

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()

    # Initialize center position at the center of the screen
    center_x = screen_width / 2
    center_y = screen_height / 2

    # Create the Icosahedron shape
    icosahedron = Icosahedron((center_x, center_y))

    while running:
        # Cap the frame rate and calculate FPS
        clock.tick(60)

        screen.fill((0, 0, 0))  # Clear the screen

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Update and draw the Icosahedron
        icosahedron.update()
        icosahedron.draw(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
