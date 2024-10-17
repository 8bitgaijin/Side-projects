import pygame
import noise  # Perlin noise library

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
SKY_BLUE = (135, 206, 235)  # Sky blue background
WHITE = (255, 255, 255)  # White cloud color for brighter clouds
BASE_ALPHA = 220  # Higher base alpha for more visible clouds
NOISE_SCALE = 0.005  # Scale to control cloud pattern size
CLOUD_THRESHOLD = 0.05  # Lower threshold to make clouds more dense
ALPHA_MULTIPLIER = 2.5  # Control how quickly alpha ramps up for denser clouds
CLOUD_SPEED = 0.5  # Speed of the cloud movement (pixels per frame)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Perlin Noise Moving Clouds Demo")

# Function to generate a Perlin noise cloud mask with horizontal offset
def generate_perlin_cloud(x_offset):
    # Create a surface for the cloud with alpha
    cloud_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # Generate Perlin noise for the entire screen
    for x in range(WIDTH):
        for y in range(HEIGHT):
            # Introduce a horizontal offset to create the movement effect
            noise_value = noise.pnoise2((x + x_offset) * NOISE_SCALE, y * NOISE_SCALE, octaves=4)
            
            # If the noise value is higher than the threshold, draw a cloud pixel
            if noise_value > CLOUD_THRESHOLD:
                # Scale the alpha based on the noise value to make smoother cloud edges
                alpha = min(int((noise_value - CLOUD_THRESHOLD) * 255 * ALPHA_MULTIPLIER), BASE_ALPHA)
                pygame.draw.circle(cloud_surface, (*WHITE, alpha), (x, y), 3)  # Larger clouds
    
    return cloud_surface

# Main loop
running = True
x_offset = 0  # Horizontal offset for cloud movement

while running:
    screen.fill(SKY_BLUE)  # Fill the screen with sky blue background
    
    # Generate the Perlin noise cloud surface with updated offset
    cloud_surface = generate_perlin_cloud(x_offset)
    
    # Blit the cloud surface onto the main screen
    screen.blit(cloud_surface, (0, 0))

    pygame.display.flip()

    # Move the clouds to the left by increasing the offset
    x_offset += CLOUD_SPEED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
