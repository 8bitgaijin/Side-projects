import pygame
import numpy as np

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

image = pygame.image.load("FFT.png").convert_alpha()
image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
original_image = image.copy()

radius = 50  # Bubble starts at 50


def invert_circle(surface, original, center, radius_val):
    """Invert colors in a circular region."""
    arr = pygame.surfarray.pixels3d(surface)
    orig_arr = pygame.surfarray.pixels3d(original)

    cx, cy = center
    h, w, _ = arr.shape

    x_start = max(0, cx - radius_val)
    x_end = min(h, cx + radius_val)
    y_start = max(0, cy - radius_val)
    y_end = min(w, cy + radius_val)

    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            if (x - cx)**2 + (y - cy)**2 <= radius_val**2:
                r, g, b = orig_arr[x, y]
                arr[x, y] = (255 - r, 255 - g, 255 - b)

    del arr
    del orig_arr


running = True
while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()

    image.blit(original_image, (0, 0))
    invert_circle(image, original_image, mouse_pos, radius)
    screen.blit(image, (0, 0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Increase bubble size
            elif event.key in [pygame.K_PLUS, pygame.K_EQUALS]:
                radius = min(200, radius + 10)

            # Decrease bubble size
            elif event.key == pygame.K_MINUS:
                radius = max(10, radius - 10)

pygame.quit()
