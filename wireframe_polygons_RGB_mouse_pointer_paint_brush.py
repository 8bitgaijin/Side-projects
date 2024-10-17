# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:33:47 2024

@author: Shane
"""

import pygame
import math
import colorsys  # For HSV to RGB conversion
import random    # For random initial rotations
from pygame.locals import *

# Initialize pygame and font module
pygame.init()
pygame.font.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('3D Shapes Painter')

# Define vertices and edges for the shapes
shapes_data = {
    'cube': {
        'vertices': [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Back face
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # Front face
        ],
        'edges': [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Back face edges
            (4, 5), (5, 6), (6, 7), (7, 4),  # Front face edges
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]
    },
    'pyramid': {
        'vertices': [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Base
            [0, 0, 1]  # Top point
        ],
        'edges': [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Base edges
            (0, 4), (1, 4), (2, 4), (3, 4)   # Side edges connecting to the top
        ]
    },
    'tetrahedron': {
        'vertices': [
            [1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]
        ],
        'edges': [
            (0, 1), (0, 2), (0, 3),
            (1, 2), (1, 3), (2, 3)
        ]
    }
}

# Projection function to convert 3D points to 2D
def project_3d_to_2d(point, center_x, center_y, fov=512, viewer_distance=10):
    """ Project a 3D point onto a 2D plane (the screen) using perspective projection. """
    factor = fov / (viewer_distance + point[2])
    x = point[0] * factor + center_x
    y = -point[1] * factor + center_y  # Invert y-axis to match Pygame's coordinate system
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

# Define the Shape class
class Shape:
    def __init__(self, shape_type, position, angle_x=None, angle_y=None, angle_z=None):
        self.shape_type = shape_type
        self.position = position  # (center_x, center_y)
        # Initialize rotation angles; if not provided, use random angles
        self.angle_x = angle_x if angle_x is not None else random.uniform(0, 2 * math.pi)
        self.angle_y = angle_y if angle_y is not None else random.uniform(0, 2 * math.pi)
        self.angle_z = angle_z if angle_z is not None else random.uniform(0, 2 * math.pi)
        # Randomize rotation speeds slightly to make animations unique
        self.rotation_speed_x = 0.01 + random.uniform(-0.005, 0.005)
        self.rotation_speed_y = 0.02 + random.uniform(-0.005, 0.005)
        self.rotation_speed_z = 0.015 + random.uniform(-0.005, 0.005)
        self.vertices = shapes_data[shape_type]['vertices']
        self.edges = shapes_data[shape_type]['edges']
        self.hue = random.random()  # Initial hue value for color cycling

    def update(self):
        # Rotate the shape slightly
        self.angle_x += self.rotation_speed_x
        self.angle_y += self.rotation_speed_y
        self.angle_z += self.rotation_speed_z

        # Update the hue value to cycle through colors
        self.hue += 0.00833  # Adjust the speed of color cycling
        if self.hue > 1.0:
            self.hue -= 1.0  # Loop the hue value

    def draw(self, screen):
        # Rotate the shape's vertices
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

        # Convert HSV to RGB with full saturation and value for bright colors
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        edge_color = (int(r * 255), int(g * 255), int(b * 255))

        # Draw the edges of the shape with the dynamic color
        for edge in self.edges:
            pygame.draw.line(
                screen, edge_color, projected_vertices[edge[0]], projected_vertices[edge[1]], 2
            )

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    current_shape_type = 'cube'  # Start with the cube

    # Initialize center position at the center of the screen
    center_x = screen_width / 2
    center_y = screen_height / 2

    # This shape follows the mouse cursor
    moving_shape = Shape(current_shape_type, (center_x, center_y))

    # List to store all the shapes that have been placed
    shapes = []

    # Initialize font for FPS counter and instructions
    font = pygame.font.SysFont(None, 24)

    # Initialize hue values for text elements
    hue_fps = 0.0          # Hue for FPS counter
    hue_instructions = 0.33  # Hue for instructions
    hue_total = 0.66        # Hue for total objects counter

    instructions = [
        "Press 'C' for Cube",
        "Press 'P' for Pyramid",
        "Press 'T' for Tetrahedron",
    ]

    while running:
        # Cap the frame rate and calculate FPS
        fps = clock.get_fps()
        clock.tick(60)

        screen.fill((0, 0, 0))  # Clear the screen

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == KEYDOWN:
                if event.key == K_c:  # 'C' for Cube
                    current_shape_type = 'cube'
                elif event.key == K_p:  # 'P' for Pyramid
                    current_shape_type = 'pyramid'
                elif event.key == K_t:  # 'T' for Tetrahedron
                    current_shape_type = 'tetrahedron'
                # Update the moving shape to the new type
                moving_shape.shape_type = current_shape_type
                moving_shape.vertices = shapes_data[current_shape_type]['vertices']
                moving_shape.edges = shapes_data[current_shape_type]['edges']
            if event.type == pygame.MOUSEMOTION:
                # Update the center position to the mouse position
                center_x, center_y = event.pos
                moving_shape.position = (center_x, center_y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    # Add the current shape to the list of shapes
                    new_shape = Shape(
                        current_shape_type,
                        (center_x, center_y),
                        moving_shape.angle_x,
                        moving_shape.angle_y,
                        moving_shape.angle_z
                    )
                    shapes.append(new_shape)

        # Update and draw all shapes
        for shape in shapes:
            shape.update()
            shape.draw(screen)

        # Update and draw the moving shape
        moving_shape.update()
        moving_shape.draw(screen)

        # Update hues
        hue_increment = 0.005  # Adjust the speed of color cycling for text
        hue_fps += hue_increment
        hue_instructions += hue_increment
        hue_total += hue_increment

        # Loop hues back to 0 when they exceed 1.0
        if hue_fps > 1.0:
            hue_fps -= 1.0
        if hue_instructions > 1.0:
            hue_instructions -= 1.0
        if hue_total > 1.0:
            hue_total -= 1.0

        # Convert hues to RGB colors
        r_fps, g_fps, b_fps = colorsys.hsv_to_rgb(hue_fps, 1.0, 1.0)
        fps_color = (int(r_fps * 255), int(g_fps * 255), int(b_fps * 255))

        r_instr, g_instr, b_instr = colorsys.hsv_to_rgb(hue_instructions, 1.0, 1.0)
        instructions_color = (int(r_instr * 255), int(g_instr * 255), int(b_instr * 255))

        r_total, g_total, b_total = colorsys.hsv_to_rgb(hue_total, 1.0, 1.0)
        total_color = (int(r_total * 255), int(g_total * 255), int(b_total * 255))

        # Render FPS counter
        fps_text = font.render(f'FPS: {int(fps)}', True, fps_color)
        screen.blit(fps_text, (10, 10))

        # Render instructions
        for i, line in enumerate(instructions):
            instruction_text = font.render(line, True, instructions_color)
            screen.blit(instruction_text, (10, 30 + i * 20))

        # Render total number of objects
        total_objects = len(shapes)
        total_objects_text = font.render(f'Total Objects: {total_objects}', True, total_color)
        # Position the text under the instructions
        text_y_position = 30 + len(instructions) * 20 + 10  # 10 pixels gap
        screen.blit(total_objects_text, (10, text_y_position))

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
