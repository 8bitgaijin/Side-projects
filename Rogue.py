import pygame
import random
import time  # To get the current system time

# Initialize Pygame
pygame.init()

# Set up display constants
WIDTH, HEIGHT = 640, 480
FONT_SIZE = 16
FONT = pygame.font.SysFont("monospace", FONT_SIZE)

# Set up color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the dungeon size and player starting position
DUNGEON_WIDTH = 40
DUNGEON_HEIGHT = 25
player_x, player_y = 0, 0  # We will set this later when we spawn the player

# Define the player using a dictionary
player = {
    "name": "Adventurer",  # This will be updated
    "level": 1,
    "HP": 10,              # Health Points (formerly hits)
    "str": 5,              # Strength
    "armor": 0,            # Armor value
    "exp": 0,              # Experience points
    "gold": 0              # Gold
}






# Dungeon map (2D array of ASCII characters)
dungeon = [['#'] * DUNGEON_WIDTH for _ in range(DUNGEON_HEIGHT)]

# Add some rooms to the dungeon (very basic random generation)
def generate_dungeon():
    global dungeon
    for i in range(1, DUNGEON_HEIGHT - 1):
        for j in range(1, DUNGEON_WIDTH - 1):
            dungeon[i][j] = '.' if random.random() > 0.2 else '#'

# Ensure a safe spawn location for the player
def spawn_player():
    global player_x, player_y
    while True:
        player_x = random.randint(1, DUNGEON_WIDTH - 2)
        player_y = random.randint(1, DUNGEON_HEIGHT - 2)
        if dungeon[player_y][player_x] == '.':
            break

# Simple flood fill algorithm to ensure there's a valid path from the player's spawn
def flood_fill_check(x, y):
    visited = [[False] * DUNGEON_WIDTH for _ in range(DUNGEON_HEIGHT)]
    to_visit = [(x, y)]
    
    while to_visit:
        cx, cy = to_visit.pop()
        if cx < 0 or cy < 0 or cx >= DUNGEON_WIDTH or cy >= DUNGEON_HEIGHT:
            continue
        if visited[cy][cx] or dungeon[cy][cx] == '#':
            continue
        visited[cy][cx] = True
        
        # Add neighboring positions to visit if they are valid
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < DUNGEON_WIDTH and 0 <= ny < DUNGEON_HEIGHT and not visited[ny][nx]:
                to_visit.append((nx, ny))

    # Check if we have a valid path (at least one other open tile is reachable)
    return any(visited[y][x] and dungeon[y][x] == '.' for x in range(DUNGEON_WIDTH) for y in range(DUNGEON_HEIGHT))

# Draw the current time in HH:MM format in the bottom right corner
def draw_clock(screen):
    current_time = time.strftime("%H:%M")  # Get current time in HH:MM format
    clock_x = WIDTH - (len(current_time) * FONT_SIZE * 0.55)  # Align to the right
    clock_y = HEIGHT - FONT_SIZE  # Align to the bottom
    draw_text(screen, current_time, clock_x // FONT_SIZE, clock_y // FONT_SIZE)

# Draw the ASCII dungeon to the screen
def draw_dungeon(screen):
    global dungeon
    screen.fill(BLACK)
    for y in range(DUNGEON_HEIGHT):
        for x in range(DUNGEON_WIDTH):
            draw_text(screen, dungeon[y][x], x, y)
    draw_text(screen, '☺', player_x, player_y)  # Draw the player as a smiley face
    
    # Use the player's name from the player dictionary
    draw_text(screen, f"Adventurer: {player['name']}", 0, DUNGEON_HEIGHT)  # Show player name
    draw_text(screen, f"Level: {player['level']}", 0, DUNGEON_HEIGHT + 1)
    draw_text(screen, f"HP: {player['HP']}", 0, DUNGEON_HEIGHT + 2)
    draw_text(screen, f"STR: {player['str']}", 0, DUNGEON_HEIGHT + 3)
    draw_text(screen, f"Armor: {player['armor']}", 15, DUNGEON_HEIGHT)
    draw_text(screen, f"EXP: {player['exp']}", 15, DUNGEON_HEIGHT + 1)
    draw_text(screen, f"Gold: {player['gold']}", 15, DUNGEON_HEIGHT + 2)
    
    # Call the clock drawing function
    draw_clock(screen)
    
    # Example of how to access the player's attributes
    # print(f"Player Name: {player['name']}")
    # print(f"Player Level: {player['level']}")

    # print(f"Player Strength: {player['str']}")
    # print(f"Player Gold: {player['gold']}")
    # # Example usage
    # print(f"Player's name: {player['name']}")
    # print(f"Player's HP: {player['HP']}")
    # print(f"Player's armor: {player['armor']}")
    # print(f"Player's experience: {player['exp']}")

    pygame.display.flip()


# Helper function to draw text at a specific grid location
def draw_text(screen, text, x, y):
    label = FONT.render(text, 1, WHITE)
    screen.blit(label, (x * FONT_SIZE, y * FONT_SIZE))

# Move player if the new position is within bounds and not a wall
def move_player(dx, dy):
    global player_x, player_y
    new_x = player_x + dx
    new_y = player_y + dy
    if 0 <= new_x < DUNGEON_WIDTH and 0 <= new_y < DUNGEON_HEIGHT:
        if dungeon[new_y][new_x] != '#':  # Prevent walking through walls
            player_x = new_x
            player_y = new_y

# Main game loop
def game_loop():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move_player(-1, 0)
        if keys[pygame.K_RIGHT]:
            move_player(1, 0)
        if keys[pygame.K_UP]:
            move_player(0, -1)
        if keys[pygame.K_DOWN]:
            move_player(0, 1)

        draw_dungeon(screen)
        clock.tick(10)

# Get player name function
# Update the get_player_name function to modify the player's name
def get_player_name():
    # Define positions and sizes with descriptive variables
    input_box_width = 400
    input_box_height = 40
    input_box_x = WIDTH // 4  # Center the input box horizontally (1/4 of the screen width)
    input_box_y = HEIGHT // 2 - input_box_height  # Position the input box vertically (middle of the screen)
    
    text_offset_x = 5  # Horizontal padding inside the input box for the text
    text_offset_y = 5  # Vertical padding inside the input box for the text
    
    prompt_x = 0  # Align the prompt with the input box horizontally
    prompt_y = 0  # Place the prompt above the input box

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)  # Create the input box

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if len(text) > 0:  # Only accept if name is not empty
                            player['name'] = text  # Update the player's name in the dictionary
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        # Allow only alphabetic characters and limit to 10 characters
                        if event.unicode.isalpha() and len(text) < 10:
                            text += event.unicode

        screen.fill(BLACK)

        # Render the input box text
        txt_surface = FONT.render(text, True, WHITE)
        
        # Adjust input box width based on text length to prevent shrinking
        width = max(input_box_width, txt_surface.get_width() + 10)
        input_box.w = width

        # Draw the text inside the input box with offset
        screen.blit(txt_surface, (input_box.x + text_offset_x, input_box.y + text_offset_y))
        
        # Draw the rectangular input box
        pygame.draw.rect(screen, color, input_box, 2)

        # Draw the prompt text
        draw_text(screen, "Enter your adventurer's name (max 10 chars):", prompt_x, prompt_y)

        pygame.display.flip()


# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASCII Roguelike")

# Get the player's name before starting the game
get_player_name()

# Generate the dungeon
generate_dungeon()

# Spawn the player in a safe location
spawn_player()

# Start the game loop
game_loop()

pygame.quit()
