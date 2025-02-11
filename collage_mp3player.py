# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:20:34 2024

@author: Shane
"""

import pygame
import os
import random
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RIGHT, K_LEFT

# Initialize pygame
pygame.init()

# Hard-code the resolution to 1920x1080 for fullscreen mode
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Variables for controlling draw speed (milliseconds between images) and max tilt angle
DRAW_SPEED = 500
MAX_ANGLE = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Photo Collage')

# Directory to look for images and music
PICTURES_FOLDER = os.path.join(os.getcwd(), "pictures")
MUSIC_FOLDER = os.path.join(os.getcwd(), "music")

# Music list and playback variables
music_list = []
current_track_index = 0
current_track_name = ""

# Initialize fonts for displaying text
pygame.font.init()
FONT = pygame.font.Font(None, 36)  # Default font with size 36

# Variable to track the area where the text was previously drawn
previous_text_rect = None

# Function to load all mp3 files recursively from the music folder
def load_music_files():
    global music_list
    for root, _, files in os.walk(MUSIC_FOLDER):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                music_list.append(file_path)
    
    # Randomize the music list but maintain track order for skipping
    random.shuffle(music_list)

# Function to play the current track from the list
def play_current_track():
    global current_track_name
    if not music_list:
        return
    
    current_track_path = music_list[current_track_index]
    current_track_name = os.path.splitext(os.path.basename(current_track_path))[0]  # Extract filename without extension

    pygame.mixer.init()
    pygame.mixer.music.load(current_track_path)
    pygame.mixer.music.play()

    # Print the current playing track's information (filename only)
    print(f"Now playing: {current_track_name}")

# Function to skip to the next track
def play_next_track():
    global current_track_index
    if not music_list:
        return
    
    current_track_index = (current_track_index + 1) % len(music_list)
    play_current_track()

# Function to go back to the previous track
def play_previous_track():
    global current_track_index
    if not music_list:
        return

    current_track_index = (current_track_index - 1) % len(music_list)
    play_current_track()

# Function to display the current track name at the bottom-left of the screen with drop shadow
def display_current_track_name():
    global previous_text_rect

    # Erase the old text by filling the previous text area with black
    if previous_text_rect:
        screen.fill((0, 0, 0), previous_text_rect)

    # Create shadow text surface
    shadow_surface = FONT.render(current_track_name, True, (0, 0, 0))  # Black color for shadow
    shadow_position = (12, SCREEN_HEIGHT - 38)  # Offset slightly to the bottom-right for the shadow

    # Create main text surface
    text_surface = FONT.render(current_track_name, True, (255, 255, 255))  # White color for main text
    text_position = (10, SCREEN_HEIGHT - 40)  # Position at bottom-left with slight padding

    # Blit the shadow first, then the main text
    screen.blit(shadow_surface, shadow_position)
    screen.blit(text_surface, text_position)

    # Update previous_text_rect to the latest text position and size
    previous_text_rect = text_surface.get_rect(topleft=text_position)

# Function to initialize the screen with a black fill
def initialize_screen():
    screen.fill((0, 0, 0))

# Function to quit Pygame properly
def quit_pygame():
    pygame.quit()

# Function to get all the current events
def get_events():
    return pygame.event.get()

# Function to handle quit events
def handle_quit_event(event):
    if event.type == pygame.QUIT:
        return False
    return True

# Function to handle keyboard events, such as pressing escape or changing tracks
def handle_keyboard_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == K_ESCAPE:
            return False
        elif event.key == K_RIGHT:  # Right arrow to skip to the next track
            play_next_track()
        elif event.key == K_LEFT:  # Left arrow to go to the previous track
            play_previous_track()
    return True

# Main function to handle events
def handle_events():
    for event in get_events():
        if not handle_quit_event(event) or not handle_keyboard_event(event):
            return False
    return True    

# Function to load a random image from the pictures folder
def load_random_image():
    valid_extensions = ['.png', '.jpg', '.jpeg']
    image_files = [f for f in os.listdir(PICTURES_FOLDER) 
                   if os.path.isfile(os.path.join(PICTURES_FOLDER, f)) and 
                   os.path.splitext(f)[1].lower() in valid_extensions]

    if not image_files:
        return None  # Return None if no valid images are found

    random_image_path = os.path.join(PICTURES_FOLDER, random.choice(image_files))
    # Ensure the image retains transparency
    return pygame.image.load(random_image_path).convert_alpha()  

# Function to scale an image to fit within the screen dimensions
def scale_image(image):
    if image is None:
        return None

    image_width, image_height = image.get_size()
    max_scale_factor = min(SCREEN_WIDTH / image_width, SCREEN_HEIGHT / image_height)

    # Pick a random scale factor between 0.2 and the maximum scale factor
    scale_factor = random.uniform(0.2, min(0.8, max_scale_factor))
    new_width = int(image_width * scale_factor)
    new_height = int(image_height * scale_factor)

    return pygame.transform.scale(image, (new_width, new_height))

# Function to tilt an image randomly by a certain angle
def tilt_image(image):
    if image is None:
        return None

    # Rotate the image by a random angle between -MAX_ANGLE and +MAX_ANGLE, excluding 0 degrees
    tilt_angle = random.choice([random.uniform(-MAX_ANGLE, -5), random.uniform(5, MAX_ANGLE)])
    return pygame.transform.rotate(image, tilt_angle)

# Main function to load, scale, and tilt the image
def load_scale_and_tilt_random_image():
    image = load_random_image()
    scaled_image = scale_image(image)
    tilted_image = tilt_image(scaled_image)
    return tilted_image

# Function to calculate a random position on the screen where the image can be fully displayed
def get_random_position(image_width, image_height):
    x_pos = random.randint(0, max(0, SCREEN_WIDTH - image_width))
    y_pos = random.randint(0, max(0, SCREEN_HEIGHT - image_height))
    return x_pos, y_pos

# Function to draw the image at a given position on the screen
def draw_image_at_position(image, position):
    if image is None:
        return

    screen.blit(image, position)

# Updated version of draw_image_at_random_position
def draw_image_at_random_position(image):
    if image is None:
        return

    image_width, image_height = image.get_size()
    random_position = get_random_position(image_width, image_height)
    draw_image_at_position(image, random_position)

# Function to handle drawing the collage step by step
def draw_collage_step():
    # Load, scale, and tilt a random image
    random_image = load_scale_and_tilt_random_image()
    # Draw the image at a random position on the screen
    draw_image_at_random_position(random_image)

# Function to update the display with the current screen content
def update_display():
    pygame.display.flip()

# Function to delay based on draw speed
def apply_draw_delay():
    pygame.time.delay(DRAW_SPEED)

# Main loop for photo collage
def photo_collage():
    initialize_screen()  # Start with a black screen
    running = True

    # Load music files and start playing
    load_music_files()
    if music_list:
        play_current_track()

    while running:
        # Handle the events
        if not handle_events():
            break

        # Draw the collage step-by-step
        draw_collage_step()

        # Display the current track name at the bottom-left
        display_current_track_name()

        # Update the display but do not clear the screen, letting the images overlap
        update_display()

        # Delay based on the draw speed
        apply_draw_delay()

    quit_pygame()

if __name__ == "__main__":
    photo_collage()
