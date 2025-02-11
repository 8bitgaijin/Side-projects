# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:47:44 2024

@author: Shane
"""

import pygame
import pyttsx3
import ctypes
import threading
from pygame.locals import *
import os

# Initialize pygame and set up the screen
pygame.init()

# Query for the monitor's resolution
user32 = ctypes.windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Set window dimensions
window_width, window_height = 800, 600
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

# Set window position and create the window
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("My Pygame Project")

# Bring window to the front
user32.SetForegroundWindow(pygame.display.get_wm_info()['window'])

# Lock to manage TTS access
tts_lock = threading.Lock()

def speak(text):
    """Threaded function to handle TTS without queuing by resetting engine."""
    with tts_lock:
        engine = pyttsx3.init()  # Re-initialize the TTS engine to cancel any ongoing speech
        engine.say(text)
        engine.runAndWait()
        engine.stop()

def start_tts(text):
    """Start TTS in a new daemon thread to prevent queuing."""
    tts_thread = threading.Thread(target=speak, args=(text,), daemon=True)
    tts_thread.start()

# Conversation dictionary with defined nodes
conversation = {
    0: {
        "prompt": "Hi there! I'm here to chat with you. How can I assist?",
        "responses": ["Tell me more about you.", "I just want to say hi.", "What can you do?"],
        "next_nodes": [1, 2, 3]
    },
    1: {
        "prompt": "I'm a simple chatbot, here to answer questions or have a chat! What would you like to know?",
        "responses": ["What can you tell me?", "How do I use this bot?", "Just saying thanks!"],
        "next_nodes": [3, 2, 0]
    },
    2: {
        "prompt": "Well, hello! Nice to meet you! Do you need help with something, or just here to chat?",
        "responses": ["Just here to chat!", "Need some help!", "Tell me a fun fact."],
        "next_nodes": [0, 1, 3]
    },
    3: {
        "prompt": "I can chat with you and keep things interesting! What's on your mind?",
        "responses": ["Just curious!", "Nothing for now.", "Tell me a joke!"],
        "next_nodes": [2, 1, 0]
    },
}

# Chatbot variables
current_node = 0  # Start with the greeting node

def render_conversation(node_id):
    """Render the chatbot's current prompt and responses on the screen."""
    node = conversation[node_id]
    screen.fill((0, 0, 0))  # Clear screen with black background
    font = pygame.font.SysFont(None, 36)

    # Render the chatbot's prompt
    prompt_surface = font.render(node["prompt"], True, (255, 255, 255))
    screen.blit(prompt_surface, (50, 50))

    # Render each response option
    for i, response in enumerate(node["responses"]):
        response_surface = font.render(f"{i + 1}. {response}", True, (200, 200, 200))
        screen.blit(response_surface, (50, 150 + i * 40))

def handle_user_input(key, node_id):
    """Handle user input to choose a response and navigate conversation."""
    global current_node
    node = conversation[node_id]
    if key in [K_1, K_2, K_3]:  # Only handle keys 1, 2, or 3 for simplicity
        choice_index = key - K_1
        if choice_index < len(node["next_nodes"]):
            current_node = node["next_nodes"][choice_index]
            start_tts(conversation[current_node]["prompt"])  # Trigger TTS in a new thread

# Start initial TTS
start_tts(conversation[current_node]["prompt"])

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            handle_user_input(event.key, current_node)

    render_conversation(current_node)
    pygame.display.flip()
    pygame.time.Clock().tick(30)  # Cap the frame rate

# Quit pygame
pygame.quit()
