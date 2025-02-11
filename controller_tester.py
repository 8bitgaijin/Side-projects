import pygame
import sys

# Initialize Pygame
pygame.init()

# Window size
WIDTH, HEIGHT = 640, 480

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Controller Test")

# Initialize joystick
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    # Output controller info
    print(f"Controller Name: {joystick.get_name()}")
    print(f"Number of Axes: {joystick.get_numaxes()}")
    print(f"Number of Buttons: {joystick.get_numbuttons()}")
    print(f"Number of Hats (D-Pads): {joystick.get_numhats()}")
else:
    print("No controller connected!")
    joystick = None

def main():
    clock = pygame.time.Clock()
    background_color = (0, 0, 0)  # Default to black

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if joystick:
            button_pressed = False

            # Check if any button is pressed
            for button in range(joystick.get_numbuttons()):
                if joystick.get_button(button):
                    button_pressed = True
                    print(f"Button {button} pressed!")
                    break  # Only log one button at a time

            # Check D-pad via axes
            for axis in range(joystick.get_numaxes()):
                axis_value = joystick.get_axis(axis)
                if abs(axis_value) > 0.1:  # Threshold to ignore small values
                    button_pressed = True
                    print(f"Axis {axis} moved: {axis_value:.2f}")

            # Change background color when a button or D-pad is pressed
            if button_pressed:
                background_color = (0, 255, 0)  # Green for "lit up"
            else:
                background_color = (0, 0, 0)  # Default to black

        # Fill the screen with the current background color
        screen.fill(background_color)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
