import pygame
import numpy as np
import time  # Import time module to calculate elapsed time

# Constants
WIDTH, HEIGHT = 400, 400
MAX_ITER = 100  # Lower the iteration for speed
ZOOM = 200
OFFSET = (-0.75, 0.0)

# Mandelbrot calculation
def mandelbrot(c):
    z = c
    for n in range(MAX_ITER):
        if abs(z) > 2:
            return n
        z = z * z + c
    return MAX_ITER

# Map pixel to complex plane
def pixel_to_complex(x, y, width, height, zoom, offset):
    real = (x - width / 2) / zoom + offset[0]
    imag = (y - height / 2) / zoom + offset[1]
    return complex(real, imag)

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mandelbrot Set")
    
    # Surface to store pixels
    surface = pygame.Surface((WIDTH, HEIGHT))
    
    # Record the start time
    start_time = time.time()

    # Generate Mandelbrot set and display it incrementally
    for x in range(WIDTH):
        for y in range(HEIGHT):
            c = pixel_to_complex(x, y, WIDTH, HEIGHT, ZOOM, OFFSET)
            color_value = mandelbrot(c)
            
            # Color based on iteration count
            color = (color_value % 8 * 32, color_value % 16 * 16, color_value % 32 * 8)
            surface.set_at((x, y), color)
        
        # Incremental display to avoid long wait
        if x % 10 == 0:
            screen.blit(surface, (0, 0))
            pygame.display.flip()

    pygame.display.flip()

    # Record the end time
    end_time = time.time()

    # Calculate and print the total time
    total_time = end_time - start_time
    print(f"Time taken to generate the Mandelbrot set: {total_time:.2f} seconds")

    # Event loop to exit on ESC
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
