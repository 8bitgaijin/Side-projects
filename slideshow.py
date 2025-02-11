import math
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





# In
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

def fade_in(screen, new_image, clock):
    alpha = 0  # Start with fully transparent
    new_image.set_alpha(alpha)  # Set initial transparency
    while alpha < 255:  # Loop until fully opaque
        screen.fill((0, 0, 0))  # Clear the screen with black
        new_image.set_alpha(alpha)  # Set the current transparency
        screen.blit(new_image, (0, 0))  # Blit the image with transparency
        pygame.display.flip()  # Update the display
        alpha += 5  # Increase transparency gradually
        clock.tick(60)  # Control the frame rate

        # Handle events during the transition
        if not handle_events():
            return False
    return True

def zoom_in(screen, new_image, clock):
    scale = 0.1  # Start with the image scaled down to 10%
    while scale < 1.0:  # Loop until the image reaches full size (100%)
        # screen.fill((0, 0, 0))  # Clear the screen with black
        scaled_image = pygame.transform.scale(new_image, (int(new_image.get_width() * scale), int(new_image.get_height() * scale)))  # Scale the image
        screen.blit(scaled_image, ((screen_width - scaled_image.get_width()) // 2, (screen_height - scaled_image.get_height()) // 2))  # Center the image
        pygame.display.flip()  # Update the display
        scale += 0.05  # Gradually increase the scale
        clock.tick(60)  # Control the frame rate

        # Handle events during the transition
        if not handle_events():
            return False
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

def rotate_in(screen, new_image, clock):
    angle = 180  # Start the image rotated by 90 degrees
    while angle > 0:  # Rotate until the image is upright (0 degrees)
        screen.fill((0, 0, 0))  # Clear the screen with black
        rotated_image = pygame.transform.rotate(new_image, angle)  # Rotate the image
        rotated_rect = rotated_image.get_rect(center=(screen_width // 2, screen_height // 2))  # Center the rotated image
        screen.blit(rotated_image, rotated_rect.topleft)  # Blit the rotated image to the screen
        pygame.display.flip()  # Update the display
        angle -= 5  # Gradually decrease the angle
        clock.tick(60)  # Control the frame rate

        # Handle events during the transition
        if not handle_events():
            return False
    return True

def bounce_in(screen, new_image, clock):
    image_width, image_height = new_image.get_size()
    x_pos = -image_width  # Start off-screen to the left
    y_pos = screen_height - image_height  # Start at the bottom of the screen

    # Calculate total distance to travel to the center
    total_distance = (screen_width - image_width) // 2

    # Ensure total_distance is not zero, which could happen if the image width equals the screen width
    if total_distance == 0:
        total_distance = screen_width // 4  # Set a minimum distance to prevent zero division

    bounce_peaks = 2  # Number of bounces

    while x_pos < (screen_width - image_width) // 2:  # Loop until it reaches the center
        screen.fill((0, 0, 0))  # Clear the screen with black
        
        # Progress is the percentage of how far the image has traveled along the x-axis (clamped to 0.0 - 1.0)
        progress = (x_pos + image_width) / total_distance
        
        # Adjust y position to create exactly two bounces using sine wave
        # abs(math.sin(progress * math.pi)) creates one bounce per pi period
        # Multiply by the number of peaks (2) and normalize with math.pi for smooth bounces
        y_pos = screen_height - image_height - int((1/3) * screen_height * abs(math.sin(progress * math.pi * bounce_peaks / 2)))

        # Blit the image at the current x and y positions
        screen.blit(new_image, (x_pos, y_pos))
        pygame.display.flip()  # Update the display
        
        x_pos += 15  # Move the image to the right
        clock.tick(60)  # Control the frame rate
        
        # Handle events during the transition
        if not handle_events():
            return False
    
    return True


def zoom_and_fade_in(screen, new_image, clock):
    image_width, image_height = new_image.get_size()
    scale = 0.1  # Start with the image at 10% of its size
    alpha = 0  # Start with fully transparent
    new_image.set_alpha(alpha)  # Set initial transparency

    while scale < 1.0:  # Loop until the image reaches full size
        screen.fill((0, 0, 0))  # Clear the screen with black

        # Scale the image
        scaled_image = pygame.transform.scale(new_image, (int(image_width * scale), int(image_height * scale)))
        scaled_image.set_alpha(alpha)  # Apply current transparency level

        # Center the image on the screen
        screen.blit(scaled_image, ((screen_width - scaled_image.get_width()) // 2, (screen_height - scaled_image.get_height()) // 2))
        pygame.display.flip()  # Update the display

        scale += 0.02  # Gradually increase the scale
        alpha = min(255, alpha + 5)  # Gradually increase the transparency (0 to 255)

        clock.tick(60)  # Control the frame rate

        # Handle events during the transition
        if not handle_events():
            return False
    
    return True






# Out
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

def fade_out(screen, image, clock):
    alpha = 255  # Start fully opaque
    image.set_alpha(alpha)  # Set initial transparency
    while alpha > 0:  # Loop until fully transparent
        screen.fill((0, 0, 0))  # Clear the screen with black
        image.set_alpha(alpha)  # Set the current transparency
        screen.blit(image, (0, 0))  # Blit the image with transparency
        pygame.display.flip()  # Update the display
        alpha -= 5  # Decrease transparency gradually
        clock.tick(60)  # Control the frame rate

        # Handle events during the transition
        if not handle_events():
            return False
    return True

def zoom_out(screen, image, clock):
    scale = 1.0  # Start with the image at full size (100%)
    while scale > 0.1:  # Loop until the image scales down to 10%
        screen.fill((0, 0, 0))  # Clear the screen with black
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))  # Scale the image
        screen.blit(scaled_image, ((screen_width - scaled_image.get_width()) // 2, (screen_height - scaled_image.get_height()) // 2))  # Center the image
        pygame.display.flip()  # Update the display
        scale -= 0.05  # Gradually decrease the scale
        clock.tick(60)  # Control the frame rate

        # Handle events during the transition
        if not handle_events():
            return False
    return True

def rotate_out(screen, image, clock):
    angle = 0  # Start with the image upright
    while angle < 180:  # Rotate until the image reaches 90 degrees
        screen.fill((0, 0, 0))  # Clear the screen with black
        rotated_image = pygame.transform.rotate(image, angle)  # Rotate the image
        rotated_rect = rotated_image.get_rect(center=(screen_width // 2, screen_height // 2))  # Center the rotated image
        screen.blit(rotated_image, rotated_rect.topleft)  # Blit the rotated image to the screen
        pygame.display.flip()  # Update the display
        angle += 5  # Gradually increase the angle
        clock.tick(60)  # Control the frame rate

        # Handle events during the transition
        if not handle_events():
            return False
    return True

def bounce_out(screen, image, clock):
    image_width, image_height = image.get_size()
    
    offset = screen_width // 2

    # Start off-screen to the left, just like bounce_in
    x_pos = -image_width + offset  # Start fully off-screen
    y_pos = screen_height - image_height  # Start at the bottom of the screen

    # Calculate total distance to travel to the center
    total_distance = (screen_width - image_width) // 2

    # Ensure total_distance is not zero, which could happen if the image width equals the screen width
    if total_distance == 0:
        total_distance = screen_width // 4  # Set a minimum distance to prevent zero division

    bounce_peaks = 2  # Number of bounces

    while x_pos < total_distance:  # Loop until it reaches the center (adjusted by total_distance)
        screen.fill((0, 0, 0))  # Clear the screen with black
        
        # Progress is the percentage of how far the image has traveled along the x-axis (clamped to 0.0 - 1.0)
        progress = (x_pos + image_width) / total_distance

        # Adjust y position to create exactly two bounces using sine wave
        y_pos = screen_height - image_height - int((1/3) * screen_height * abs(math.sin(progress * math.pi * bounce_peaks / 2)))

        # ADD THE OFFSET (960) to the x_pos AFTER calculating the x position
        screen.blit(image, (x_pos + offset, y_pos))  # Add the 960 offset here
        pygame.display.flip()  # Update the display

        x_pos += 15  # Move the image to the right
        clock.tick(60)  # Control the frame rate
        
        # Handle events during the transition
        if not handle_events():
            return False

    return True










def zoom_and_fade_out(screen, image, clock):
    image_width, image_height = image.get_size()
    scale = 1.0  # Start at full size
    alpha = 255  # Start with full opacity

    while scale < 2.0:  # Continue zooming in until the image is twice the size
        screen.fill((0, 0, 0))  # Clear the screen with black

        # Scale the image
        scaled_image = pygame.transform.scale(image, (int(image_width * scale), int(image_height * scale)))
        scaled_image.set_alpha(alpha)  # Apply current transparency level

        # Center the image on the screen
        screen.blit(scaled_image, ((screen_width - scaled_image.get_width()) // 2, (screen_height - scaled_image.get_height()) // 2))
        pygame.display.flip()  # Update the display

        scale += 0.02  # Gradually increase the scale (zooming in further)
        alpha = max(0, alpha - 5)  # Gradually decrease the transparency (fade out)

        clock.tick(60)  # Control the frame rate

        # Handle events during the transition
        if not handle_events():
            return False
    
    return True





# Add the bounce transition option to the random_slide_in function
def random_slide_in(screen, new_image, clock):
    transition = random.choice([
        slide_in_from_right, 
                                slide_in_from_left, 
                                slide_in_from_bottom, 
                                fade_in, 
                                zoom_in, 
                                rotate_in, 
                                bounce_in,
                                zoom_and_fade_in
                                ])
    if not transition(screen, new_image, clock):
        return None
    return transition  # Return the transition function to know how it entered

# Modify the perform_exit function to handle bounce out
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
    elif entry_function == fade_in:
        if not fade_out(screen, image, clock):
            return False
    elif entry_function == zoom_in:
        if not zoom_out(screen, image, clock):
            return False
    elif entry_function == rotate_in:
        if not rotate_out(screen, image, clock):
            return False
    elif entry_function == bounce_in:
        if not bounce_out(screen, image, clock):
            return False
    elif entry_function == zoom_and_fade_in:
        if not zoom_and_fade_out(screen, image, clock):
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

                # Ensure the image is fully opaque after transition
                new_image.set_alpha(255)  # Reset image to full opacity

                current_image = new_image
                hang_start_time = pygame.time.get_ticks() + hang_time  # Set the end of the hang time
                in_hang_time = True  # Enter hang time

        # During hang time, display the image fully visible and correctly scaled
        if in_hang_time:
            screen.fill((0, 0, 0))  # Clear the screen with black
            screen.blit(current_image, ((screen_width - current_image.get_width()) // 2, (screen_height - current_image.get_height()) // 2))  # Display the image fully visible
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
