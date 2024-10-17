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
    'hypercube': {
        'vertices': [
            # Define the 16 vertices of a hypercube in 4D space
            # All combinations of -1 and 1 for x, y, z, w
            [-1, -1, -1, -1],  # 0
            [1, -1, -1, -1],   # 1
            [1, 1, -1, -1],    # 2
            [-1, 1, -1, -1],   # 3
            [-1, -1, 1, -1],   # 4
            [1, -1, 1, -1],    # 5
            [1, 1, 1, -1],     # 6
            [-1, 1, 1, -1],    # 7
            [-1, -1, -1, 1],   # 8
            [1, -1, -1, 1],    # 9
            [1, 1, -1, 1],     # 10
            [-1, 1, -1, 1],    # 11
            [-1, -1, 1, 1],    # 12
            [1, -1, 1, 1],     # 13
            [1, 1, 1, 1],      # 14
            [-1, 1, 1, 1]      # 15
        ],
        'edges': [
            # Edges connecting vertices in 4D space
            # Edges of the first cube (w = -1)
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
            # Edges connecting corresponding vertices between the cubes (w = -1 and w = 1)
            (0, 8), (1, 9), (2, 10), (3, 11),
            (4, 12), (5, 13), (6, 14), (7, 15),
            # Edges of the second cube (w = 1)
            (8, 9), (9, 10), (10, 11), (11, 8),
            (12, 13), (13, 14), (14, 15), (15, 12),
            (8, 12), (9, 13), (10, 14), (11, 15)
        ]
    }
}

# Projection function to convert 3D points to 2D
def project_3d_to_2d(point, center_x, center_y, fov=512, viewer_distance=10):
    """
    Project a 3D point onto a 2D plane (the screen) using perspective projection.

    Parameters:
    - point: The 3D point to project.
    - center_x, center_y: The center of the screen.
    - fov: Field of view; affects the scaling factor.
    - viewer_distance: Distance from the viewer to the screen along the Z-axis.

    Returns:
    - A tuple (x, y) representing the 2D coordinates on the screen.
    """
    factor = fov / (viewer_distance + point[2])
    x = point[0] * factor + center_x
    y = -point[1] * factor + center_y  # Invert y-axis to match Pygame's coordinate system
    return (int(x), int(y))

# Functions to rotate 3D points around the axes
def rotate_x(point, angle):
    """
    Rotate a point around the X-axis.

    Parameters:
    - point: The 3D point to rotate.
    - angle: The rotation angle in radians.

    Returns:
    - The rotated point as a list [x, y, z].
    """
    y = point[1] * math.cos(angle) - point[2] * math.sin(angle)
    z = point[1] * math.sin(angle) + point[2] * math.cos(angle)
    return [point[0], y, z]

def rotate_y(point, angle):
    """
    Rotate a point around the Y-axis.

    Parameters:
    - point: The 3D point to rotate.
    - angle: The rotation angle in radians.

    Returns:
    - The rotated point as a list [x, y, z].
    """
    x = point[2] * math.sin(angle) + point[0] * math.cos(angle)
    z = point[2] * math.cos(angle) - point[0] * math.sin(angle)
    return [x, point[1], z]

def rotate_z(point, angle):
    """
    Rotate a point around the Z-axis.

    Parameters:
    - point: The 3D point to rotate.
    - angle: The rotation angle in radians.

    Returns:
    - The rotated point as a list [x, y, z].
    """
    x = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    y = point[0] * math.sin(angle) + point[1] * math.cos(angle)
    return [x, y, point[2]]

# Function to rotate 4D points
def rotate_4d(point, angles):
    """
    Rotate a point in 4D space around the various hyperplanes.

    In 4D space, rotations occur around planes defined by pairs of axes.

    Parameters:
    - point: The 4D point to rotate.
    - angles: A list of six rotation angles (in radians) for the planes:
        [angle_xy, angle_xz, angle_xw, angle_yz, angle_yw, angle_zw]

    Returns:
    - The rotated point as a list [x, y, z, w].
    """
    x, y, z, w = point
    angle_xy, angle_xz, angle_xw, angle_yz, angle_yw, angle_zw = angles

    # Rotation in the XY plane
    x, y = (
        x * math.cos(angle_xy) - y * math.sin(angle_xy),
        x * math.sin(angle_xy) + y * math.cos(angle_xy)
    )
    # Rotation in the XZ plane
    x, z = (
        x * math.cos(angle_xz) - z * math.sin(angle_xz),
        x * math.sin(angle_xz) + z * math.cos(angle_xz)
    )
    # Rotation in the XW plane
    x, w = (
        x * math.cos(angle_xw) - w * math.sin(angle_xw),
        x * math.sin(angle_xw) + w * math.cos(angle_xw)
    )
    # Rotation in the YZ plane
    y, z = (
        y * math.cos(angle_yz) - z * math.sin(angle_yz),
        y * math.sin(angle_yz) + z * math.cos(angle_yz)
    )
    # Rotation in the YW plane
    y, w = (
        y * math.cos(angle_yw) - w * math.sin(angle_yw),
        y * math.sin(angle_yw) + w * math.cos(angle_yw)
    )
    # Rotation in the ZW plane
    z, w = (
        z * math.cos(angle_zw) - w * math.sin(angle_zw),
        z * math.sin(angle_zw) + w * math.cos(angle_zw)
    )
    return [x, y, z, w]

# Function to project 4D points to 3D
def project_4d_to_3d(point, w_viewer_distance=10):
    """
    Project a 4D point onto 3D space using perspective projection along the W-axis.

    Parameters:
    - point: The 4D point to project.
    - w_viewer_distance: Distance from the viewer to the 3D hyperplane along the W-axis.

    Returns:
    - The projected 3D point as a list [x, y, z].
    """
    w = point[3]
    factor = w_viewer_distance / (w_viewer_distance + w)
    x = point[0] * factor
    y = point[1] * factor
    z = point[2] * factor
    return [x, y, z]

# Define the Shape class
class Shape:
    def __init__(self, shape_type, position, angles=None):
        """
        Initialize the Shape object.

        Parameters:
        - shape_type: Type of the shape ('cube', 'pyramid', 'tetrahedron', 'hypercube').
        - position: Tuple (center_x, center_y) representing the position on the screen.
        - angles: Initial rotation angles. For 3D shapes, a tuple (angle_x, angle_y, angle_z).
                  For the hypercube, a list of six angles.
        """
        self.shape_type = shape_type
        self.position = position  # (center_x, center_y)
        self.vertices = shapes_data[shape_type]['vertices']
        self.edges = shapes_data[shape_type]['edges']

        if shape_type == 'hypercube':
            # Initialize rotation angles for 4D
            if angles is None:
                # Six rotation angles for the six planes in 4D space
                self.angles = [random.uniform(0, 2 * math.pi) for _ in range(6)]
            else:
                self.angles = angles
            # Randomize rotation speeds for 4D
            self.rotation_speeds = [0.01 + random.uniform(-0.005, 0.005) for _ in range(6)]
        else:
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
        """
        Update the shape's rotation angles and color hue.
        """
        if self.shape_type == 'hypercube':
            # Rotate the hypercube in 4D
            self.angles = [
                angle + speed for angle, speed in zip(self.angles, self.rotation_speeds)
            ]
        else:
            # Rotate the shape in 3D
            self.angle_x += self.rotation_speed_x
            self.angle_y += self.rotation_speed_y
            self.angle_z += self.rotation_speed_z

        # Update the hue value to cycle through colors
        self.hue += 0.00833  # Adjust the speed of color cycling
        if self.hue > 1.0:
            self.hue -= 1.0  # Loop the hue value

    def draw(self, screen):
        """
        Draw the shape on the screen.

        Parameters:
        - screen: The Pygame screen surface to draw on.
        """
        if self.shape_type == 'hypercube':
            # Rotate and project the hypercube

            # Step 1: Rotate the hypercube's vertices in 4D space
            rotated_vertices_4d = []
            for vertex in self.vertices:
                rotated = rotate_4d(vertex, self.angles)
                rotated_vertices_4d.append(rotated)

            # Step 2: Project the 4D vertices to 3D space
            projected_vertices_3d = [
                project_4d_to_3d(vertex) for vertex in rotated_vertices_4d
            ]

            # Step 3: Project the 3D vertices to 2D screen coordinates
            projected_vertices = [
                project_3d_to_2d(vertex, self.position[0], self.position[1])
                for vertex in projected_vertices_3d
            ]
        else:
            # Rotate and project 3D shapes

            # Rotate the shape's vertices in 3D space
            rotated_vertices = []
            for vertex in self.vertices:
                rotated = rotate_x(vertex, self.angle_x)
                rotated = rotate_y(rotated, self.angle_y)
                rotated = rotate_z(rotated, self.angle_z)
                rotated_vertices.append(rotated)

            # Project the 3D points to 2D screen coordinates
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
        "Press 'H' for Hypercube",
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
                elif event.key == K_h:  # 'H' for Hypercube
                    current_shape_type = 'hypercube'
                # Update the moving shape to the new type
                moving_shape = Shape(current_shape_type, (center_x, center_y))
            if event.type == pygame.MOUSEMOTION:
                # Update the center position to the mouse position
                center_x, center_y = event.pos
                moving_shape.position = (center_x, center_y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    # Add the current shape to the list of shapes
                    if current_shape_type == 'hypercube':
                        # Copy the angles to preserve the current rotation state
                        new_shape = Shape(
                            current_shape_type,
                            (center_x, center_y),
                            moving_shape.angles.copy()
                        )
                    else:
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
