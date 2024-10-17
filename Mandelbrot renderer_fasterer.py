import pygame
import numpy as np
import time

# Constants
WIDTH, HEIGHT = 400, 400
MAX_ITER = 100
ZOOM = 200
OFFSET = (-0.75, 0.0)

# Vectorized Mandelbrot calculation
def mandelbrot_vectorized(real, imag):
    c = real + imag * 1j
    z = np.zeros(c.shape, dtype=np.complex64)  # Using complex64 for performance
    divtime = np.zeros(c.shape, dtype=int)
    mask = np.ones(c.shape, dtype=bool)
    
    for i in range(MAX_ITER):
        z[mask] = z[mask] ** 2 + c[mask]
        mask = np.abs(z) < 2
        divtime[mask] = i
        
    return divtime

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

    # Generate the Mandelbrot set using vectorized operations
    mandelbrot_set = mandelbrot_vectorized(real_grid.T, imag_grid.T)

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
