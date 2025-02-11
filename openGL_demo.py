# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 13:19:23 2024

@author: Shane
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame and set up an OpenGL context
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("OpenGL + Pygame Hello World")

# Set up OpenGL perspective
glClearColor(0.1, 0.2, 0.3, 1)  # Background color: dark blue-gray
gluPerspective(45, (800 / 600), 0.1, 50.0)  # FOV, aspect ratio, near and far planes
glTranslatef(0.0, 0.0, -5)  # Move the "camera" back a bit

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw a simple triangle
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)  # Red
    glVertex3f(-1, -1, 0)
    glColor3f(0, 1, 0)  # Green
    glVertex3f(1, -1, 0)
    glColor3f(0, 0, 1)  # Blue
    glVertex3f(0, 1, 0)
    glEnd()

    # Swap buffers to display the rendered frame
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
