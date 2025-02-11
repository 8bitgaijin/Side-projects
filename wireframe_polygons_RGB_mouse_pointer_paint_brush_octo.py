# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 14:51:58 2024

@author: Shane
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 13:20:30 2024

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
            [-1, -1, -1],  # 0: Back-bottom-left
            [1, -1, -1],   # 1: Back-bottom-right
            [1, 1, -1],    # 2: Back-top-right
            [-1, 1, -1],   # 3: Back-top-left
            [-1, -1, 1],   # 4: Front-bottom-left
            [1, -1, 1],    # 5: Front-bottom-right
            [1, 1, 1],     # 6: Front-top-right
            [-1, 1, 1]     # 7: Front-top-left
        ],
        'edges': [
            # Back face edges
            (0, 1), (1, 2), (2, 3), (3, 0),
            # Front face edges
            (4, 5), (5, 6), (6, 7), (7, 4),
            # Connecting edges
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
    },
    'pyramid': {
        'vertices': [
            [-1, -1, -1],  # 0: Base-back-left
            [1, -1, -1],   # 1: Base-back-right
            [1, 1, -1],    # 2: Base-front-right
            [-1, 1, -1],   # 3: Base-front-left
            [0, 0, 1]      # 4: Apex
        ],
        'edges': [
            # Base edges
            (0, 1), (1, 2), (2, 3), (3, 0),
            # Side edges connecting to the apex
            (0, 4), (1, 4), (2, 4), (3, 4)
        ]
    },
    'tetrahedron': {
        'vertices': [
            [1, 1, 1],     # 0
            [-1, -1, 1],   # 1
            [-1, 1, -1],   # 2
            [1, -1, -1]    # 3
        ],
        'edges': [
            (0, 1), (0, 2), (0, 3),
            (1, 2), (1, 3), (2, 3)
        ]
    },
    'octahedron': {
        'vertices': [
            [1, 0, 0],    # 0: Right
            [-1, 0, 0],   # 1: Left
            [0, 1, 0],    # 2: Top
            [0, -1, 0],   # 3: Bottom
            [0, 0, 1],    # 4: Front
            [0, 0, -1]    # 5: Back
        ],
        'edges': [
            # Edges connecting to the center points
            (0, 2), (0, 3), (0, 4), (0, 5),
            (1, 2), (1, 3), (1, 4), (1, 5),
            # Edges connecting the top and bottom to the front and back
            (2, 4), (2, 5), (3, 4), (3, 5)
        ]
    }
}

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

# Define the Shape class
class Shape:
    def __init__(self, shape_type, position, angles=None):
        self.shape_type = shape_type
        self.position = position  # (center_x, center_y)
        self.vertices = shapes_data[shape_type]['vertices']
        self.edges = shapes_data[shape_type]['edges']

        # Initialize rotation angles for 3D shapes
        if angles is None:
            self.angle_x = random.uniform(0, 2 * math.pi)
            self.angle_y = random.uniform(0, 2 * math.pi)
            self.angle_z = random.uniform(0, 2 * math.pi)
        else:
            self.angle_x, self.angle_y, self.angle_z = angles
        # Randomize rotation speeds slightly to make animations unique
        self.rotation_speed_x = 0.01 + random.uniform(-0.005, 0.005)
        self.rotation_speed_y = 0.02 + random.uniform(-0.005, 0.005)
        self.rotation_speed_z = 0.015 + random.uniform(-0.005, 0.005)
        self.hue = random.random()  # Initial hue value for color cycling

    def update(self):
        self.angle_x += self.rotation_speed_x
        self.angle_y += self.rotation_speed_y
        self.angle_z += self.rotation_speed_z

        # Update the hue value to cycle through colors
        self.hue += 0.00833
        if self.hue > 1.0:
            self.hue -= 1.0

    def draw(self, screen):
        # Rotate and project 3D shapes
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

    # Initialize hue values for each individual line of text
    hue_fps = 0.0
    hue_instructions = [0.1, 0.3, 0.5, 0.7]  # Separate hues for each instruction line
    hue_total = 0.9

    instructions = [
        "Press 'C' for Cube",
        "Press 'P' for Pyramid",
        "Press 'T' for Tetrahedron",
        "Press 'O' for Octahedron",  # Add instruction for Octahedron
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
                elif event.key == K_o:  # 'O' for Octahedron
                    current_shape_type = 'octahedron'
                # Update the moving shape to the new type
                moving_shape = Shape(current_shape_type, (center_x, center_y))
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
                        (moving_shape.angle_x, moving_shape.angle_y, moving_shape.angle_z)
                    )
                    shapes.append(new_shape)

        # Update and draw all shapes
        for shape in shapes:
            shape.update()
            shape.draw(screen)

        # Update and draw the moving shape
        moving_shape.update()
        moving_shape.draw(screen)

        # Update hues for the text color cycling
        hue_increment = 0.005  # Adjust the speed of color cycling for text
        hue_fps += hue_increment
        hue_total += hue_increment
        hue_instructions = [hue + hue_increment for hue in hue_instructions]

        # Loop hues back to 0 when they exceed 1.0
        if hue_fps > 1.0:
            hue_fps -= 1.0
        if hue_total > 1.0:
            hue_total -= 1.0
        hue_instructions = [hue - 1.0 if hue > 1.0 else hue for hue in hue_instructions]

        # Convert hues to RGB colors
        r_fps, g_fps, b_fps = colorsys.hsv_to_rgb(hue_fps, 1.0, 1.0)
        fps_color = (int(r_fps * 255), int(g_fps * 255), int(b_fps * 255))

        instruction_colors = [
            (int(r * 255), int(g * 255), int(b * 255))
            for r, g, b in [colorsys.hsv_to_rgb(hue, 1.0, 1.0) for hue in hue_instructions]
        ]

        r_total, g_total, b_total = colorsys.hsv_to_rgb(hue_total, 1.0, 1.0)
        total_color = (int(r_total * 255), int(g_total * 255), int(b_total * 255))

        # Render FPS counter
        fps_text = font.render(f'FPS: {int(fps)}', True, fps_color)
        screen.blit(fps_text, (10, 10))

        # Render instructions, each with its own color
        for i, (line, color) in enumerate(zip(instructions, instruction_colors)):
            instruction_text = font.render(line, True, color)
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
