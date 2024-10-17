# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:55:50 2024

@author: Shane
"""

import pygame
import numpy as np
import time
import numba

# Constants
WIDTH, HEIGHT = 400, 400
MAX_ITER = 100
ZOOM = 200
OFFSET = (-0.75, 0.0)

# Mandelbrot calculation with Numba JIT compilation
@numba.jit(nopython=True)
def mandelbrot_pixel(real, imag):
    c = complex(real, imag)
    z = c
    for i in range(MAX_ITER):
        if abs(z) > 2:
            return i
        z = z * z + c
    return MAX_ITER

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mandelbrot Set")

    # Precompute the real and imaginary parts of the complex plane
    real = np.linspace(OFFSET[0] - (WIDTH / 2) / ZOOM, OFFSET[0] + (WIDTH / 2) / ZOOM, WIDTH)
    imag = np.linspace(OFFSET[1] - (HEIGHT / 2) / ZOOM, OFFSET[1] + (HEIGHT / 2) / ZOOM, HEIGHT)

    # Generate grid of complex numbers
    real_grid, imag_grid = np.meshgrid(real, imag)

    # Record the start time
    start_time = time.time()

    # Generate the Mandelbrot set using Numba
    mandelbrot_set = np.empty((WIDTH, HEIGHT), dtype=np.int32)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            mandelbrot_set[x, y] = mandelbrot_pixel(real_grid[x, y], imag_grid[x, y])

    # Create a NumPy array to hold the color values
    color_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)

    # Map the result to colors and store them in the array
    color_array[:, :, 0] = (mandelbrot_set % 8) * 32  # Red channel
    color_array[:, :, 1] = (mandelbrot_set % 16) * 16  # Green channel
    color_array[:, :, 2] = (mandelbrot_set % 32) * 8   # Blue channel

    # Use pygame.surfarray to draw the entire array at once
    pygame.surfarray.blit_array(screen, color_array)

    pygame.display.flip()

    # Record the end time
    end_time = time.time()

    # Calculate and print the total time
    total_time = end_time - start_time
    print(f"Time taken to generate and display the Mandelbrot set: {total_time:.2f} seconds")

    # Event loop to exit on ESC
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
