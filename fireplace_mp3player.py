# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 16:11:00 2024

@author: Shane
"""

import pygame
import os
import random
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RIGHT, K_LEFT, MOUSEBUTTONDOWN

# Initialize pygame
pygame.init()

# Hard-code the resolution to 1920x1080 for fullscreen mode
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Music with Background')

# Directory to look for images and music
PICTURES_FOLDER = os.path.join(os.getcwd(), "pictures")
MUSIC_FOLDER = os.path.join(os.getcwd(), "music")

# Music list and playback variables
music_list = []
current_track_index = 0
current_track_name = ""
background_image = None

# Initialize fonts for displaying text
pygame.font.init()
FONT = pygame.font.Font(None, 48)  # Default font with size 36

# Button colors
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)
QUIT_BUTTON_COLOR = (200, 0, 0)

# Define button dimensions and positions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 100

previous_button = pygame.Rect(BUTTON_MARGIN, SCREEN_HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN,
                              BUTTON_WIDTH, BUTTON_HEIGHT)
next_button = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN,
                          SCREEN_HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN,
                          BUTTON_WIDTH, BUTTON_HEIGHT)
quit_button = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN, BUTTON_MARGIN,
                          BUTTON_WIDTH, BUTTON_HEIGHT)


# Function to load all mp3 files recursively from the music folder
def load_music_files():
    global music_list
    for root, _, files in os.walk(MUSIC_FOLDER):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                music_list.append(file_path)
    random.shuffle(music_list)


# Function to play the current track
def play_current_track():
    global current_track_name, background_image
    if not music_list:
        return
    current_track_path = music_list[current_track_index]
    current_track_name = os.path.splitext(os.path.basename(current_track_path))[0]
    pygame.mixer.init()
    pygame.mixer.music.load(current_track_path)
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set custom event for music end
    background_image = load_random_background()



def play_next_track():
    global current_track_index
    if music_list:
        current_track_index = (current_track_index + 1) % len(music_list)
        play_current_track()


def play_previous_track():
    global current_track_index
    if music_list:
        current_track_index = (current_track_index - 1) % len(music_list)
        play_current_track()


def display_current_track_name():
    text_surface = FONT.render(current_track_name, True, (255, 255, 255))
    text_rect = text_surface.get_rect(topleft=(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.1))
    background_rect = pygame.Rect(text_rect.left - 5, text_rect.top - 5,
                                   text_rect.width + 10, text_rect.height + 10)
    pygame.draw.rect(screen, (0, 0, 0), background_rect)
    screen.blit(text_surface, text_rect)


def initialize_screen():
    screen.fill((0, 0, 0))


def quit_pygame():
    pygame.quit()


def draw_button(rect, text, color, hover=False):
    pygame.draw.rect(screen, color if not hover else BUTTON_HOVER_COLOR, rect)
    text_surface = FONT.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def load_random_background():
    valid_extensions = ['.png', '.jpg', '.jpeg']
    image_files = [f for f in os.listdir(PICTURES_FOLDER)
                   if os.path.isfile(os.path.join(PICTURES_FOLDER, f)) and
                   os.path.splitext(f)[1].lower() in valid_extensions]
    if not image_files:
        return None
    random_image_path = os.path.join(PICTURES_FOLDER, random.choice(image_files))
    return pygame.image.load(random_image_path).convert()


def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
            elif event.key == K_RIGHT:
                play_next_track()
            elif event.key == K_LEFT:
                play_previous_track()
        if event.type == MOUSEBUTTONDOWN:
            if previous_button.collidepoint(event.pos):
                play_previous_track()
            elif next_button.collidepoint(event.pos):
                play_next_track()
            elif quit_button.collidepoint(event.pos):
                return False
        if event.type == pygame.USEREVENT:  # Handle music end event
            play_next_track()
    return True



def update_display():
    if background_image:
        screen.blit(background_image, (0, 0))
    display_current_track_name()
    draw_button(previous_button, "<Previous", BUTTON_COLOR, previous_button.collidepoint(pygame.mouse.get_pos()))
    draw_button(next_button, "Next>", BUTTON_COLOR, next_button.collidepoint(pygame.mouse.get_pos()))
    draw_button(quit_button, "X", QUIT_BUTTON_COLOR, quit_button.collidepoint(pygame.mouse.get_pos()))
    pygame.display.flip()


def display_backgrounds_with_music():
    initialize_screen()
    load_music_files()
    if music_list:
        play_current_track()
    running = True
    clock = pygame.time.Clock()

    while running:
        running = handle_events()
        update_display()
        clock.tick(60)

    quit_pygame()


if __name__ == "__main__":
    display_backgrounds_with_music()
