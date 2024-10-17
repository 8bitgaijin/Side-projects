import pygame
import os
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Get screen resolution for fullscreen mode
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Image Slideshow')

# Variables for controlling transition speed and hang time
transition_speed = 50  # Control how fast the images slide in/out
hang_time = 1500  # How long the image stays in place (in milliseconds)

# Function to load and scale image while maintaining aspect ratio
def load_and_scale_image(image_path):
    image = pygame.image.load(image_path)
    image_width, image_height = image.get_size()

    # Calculate scaling ratio to fit screen, maintaining aspect ratio
    scale_ratio = min(screen_width / image_width, screen_height / image_height)
    new_width = int(image_width * scale_ratio)
    new_height = int(image_height * scale_ratio)

    # Scale image to fit within the screen while maintaining aspect ratio
    scaled_image = pygame.transform.scale(image, (new_width, new_height))

    # Create a surface with black background (for letterboxing/pillarboxing)
    final_surface = pygame.Surface((screen_width, screen_height))
    final_surface.fill((0, 0, 0))  # Fill background with black

    # Center the scaled image on the screen
    final_surface.blit(scaled_image, ((screen_width - new_width) // 2, (screen_height - new_height) // 2))

    return final_surface

# Function to get all image files in the directory
def get_image_files():
    valid_extensions = ['.png', '.jpg', '.jpeg']
    return [f for f in os.listdir('.') if os.path.isfile(f) and os.path.splitext(f)[1].lower() in valid_extensions]

# Function for the sliding transition effect from the right
def slide_in_from_right(screen, new_image, clock):
    x_pos = screen_width  # Start from the right of the screen
    while x_pos > 0:
        screen.fill((0, 0, 0))  # Clear the screen with black
        screen.blit(new_image, (x_pos, 0))  # Blit the image at the current x position
        pygame.display.flip()  # Update the display
        x_pos -= transition_speed  # Move the image towards the left

        # Handle events during the transition
        if not handle_events():
            return False

        clock.tick(60)
    return True

# Function for the sliding transition effect from the left
def slide_in_from_left(screen, new_image, clock):
    x_pos = -screen_width  # Start from the left off-screen
    while x_pos < 0:
        screen.fill((0, 0, 0))  # Clear the screen with black
        screen.blit(new_image, (x_pos, 0))  # Blit the image at the current x position
        pygame.display.flip()  # Update the display
        x_pos += transition_speed  # Move the image towards the right

        # Handle events during the transition
        if not handle_events():
            return False

        clock.tick(60)
    return True

# Function to slide the image out to the right (used for exit after display)
def slide_out_to_right(screen, image, clock):
    x_pos = 0  # Start at the center
    while x_pos < screen_width:
        screen.fill((0, 0, 0))  # Clear the screen with black
        screen.blit(image, (x_pos, 0))  # Blit the image at the current x position
        pygame.display.flip()  # Update the display
        x_pos += transition_speed  # Move the image to the right

        # Handle events during the transition
        if not handle_events():
            return False

        clock.tick(60)
    return True

# Function to slide the image out to the left (used for exit after display)
def slide_out_to_left(screen, image, clock):
    x_pos = 0  # Start at the center
    while x_pos > -screen_width:
        screen.fill((0, 0, 0))  # Clear the screen with black
        screen.blit(image, (x_pos, 0))  # Blit the image at the current x position
        pygame.display.flip()  # Update the display
        x_pos -= transition_speed  # Move the image to the left

        # Handle events during the transition
        if not handle_events():
            return False

        clock.tick(60)
    return True

# Function for the sliding transition effect from the bottom
def slide_in_from_bottom(screen, new_image, clock):
    y_pos = screen_height  # Start from the bottom of the screen
    while y_pos > 0:
        screen.fill((0, 0, 0))  # Clear the screen with black
        screen.blit(new_image, (0, y_pos))  # Blit the image at the current y position
        pygame.display.flip()  # Update the display
        y_pos -= transition_speed  # Move the image upwards

        # Handle events during the transition
        if not handle_events():
            return False

        clock.tick(60)
    return True

# Function to slide the image out to the top (used for exit after display)
def slide_out_to_top(screen, image, clock):
    y_pos = 0  # Start at the center
    while y_pos > -screen_height:
        screen.fill((0, 0, 0))  # Clear the screen with black
        screen.blit(image, (0, y_pos))  # Blit the image at the current y position
        pygame.display.flip()  # Update the display
        y_pos -= transition_speed  # Move the image upwards

        # Handle events during the transition
        if not handle_events():
            return False

        clock.tick(60)
    return True


# Function to randomly select a transition effect for entering
def random_slide_in(screen, new_image, clock):
    transition = random.choice([slide_in_from_right, slide_in_from_left, slide_in_from_bottom])
    if not transition(screen, new_image, clock):
        return None
    return transition  # Return the transition function to know how it entered


# Function to perform the opposite exit after hang_time
def perform_exit(screen, image, entry_function, clock):
    if entry_function == slide_in_from_right:
        if not slide_out_to_left(screen, image, clock):
            return False
    elif entry_function == slide_in_from_left:
        if not slide_out_to_right(screen, image, clock):
            return False
    elif entry_function == slide_in_from_bottom:
        if not slide_out_to_top(screen, image, clock):
            return False
    return True


# Function to handle events continuously
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close the window button
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Escape key to quit
            return False
    return True

# Main slideshow loop
def slideshow():
    clock = pygame.time.Clock()
    image_files = get_image_files()  # Initially load image files
    last_slide_time = 0
    current_image = None
    current_transition = None
    hang_start_time = 0
    in_hang_time = False
    running = True

    while running:
        # Slide in the new image
        if not in_hang_time and (current_image is None or pygame.time.get_ticks() >= last_slide_time):
            image_files = get_image_files()  # Check for new files every time a new image is chosen
            if image_files:
                current_image_path = random.choice(image_files)  # Randomly select an image
                new_image = load_and_scale_image(current_image_path)  # Load and scale the image
                current_transition = random_slide_in(screen, new_image, clock)  # Apply a random transition effect for entry

                if not current_transition:
                    break  # Exit if quit or escape was pressed during transition

                current_image = new_image
                hang_start_time = pygame.time.get_ticks() + hang_time  # Set the end of the hang time
                in_hang_time = True  # Enter hang time

        # During hang time, display the image and check for input
        if in_hang_time:
            screen.fill((0, 0, 0))  # Clear the screen with black
            screen.blit(current_image, (0, 0))  # Keep displaying the current image
            pygame.display.flip()  # Update the screen

            if not handle_events():
                break

            # Check if hang time has elapsed
            if pygame.time.get_ticks() >= hang_start_time:
                in_hang_time = False  # Exit hang time
                if not perform_exit(screen, current_image, current_transition, clock):
                    break

            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    slideshow()
