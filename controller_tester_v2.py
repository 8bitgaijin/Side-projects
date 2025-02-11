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

joystick = None
controller_guid = None
controller_name = "Unknown Controller"

# Known controller profiles
controller_profiles = {
    "0300dafe830500006020000000000000": "Buffalo Classic USB Gamepad",
}

# Buffalo Controller Button Mapping
buffalo_button_map = {
    0: "A (0)",
    1: "B (1)",
    2: "X (2)",
    3: "Y (3)",
    4: "L (4)",
    5: "R (5)",
    6: "Select (6)",
    7: "Start (7)",
}

buffalo_axis_map = {
    (0, -1): "D-Pad Left (Axis 0, -1)",
    (0, 1): "D-Pad Right (Axis 0, 1)",
    (1, -1): "D-Pad Up (Axis 1, -1)",
    (1, 1): "D-Pad Down (Axis 1, 1)",
}

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Get controller name and GUID
    raw_name = joystick.get_name()
    controller_guid = joystick.get_guid() if hasattr(joystick, "get_guid") else "GUID not supported"

    # Identify the controller based on GUID
    if controller_guid in controller_profiles:
        controller_name = controller_profiles[controller_guid]
    else:
        controller_name = raw_name  # Use the default reported name

    # Output controller info
    print(f"Detected Controller: {controller_name}")
    print(f"GUID: {controller_guid}")
    print(f"Number of Axes: {joystick.get_numaxes()}")
    print(f"Number of Buttons: {joystick.get_numbuttons()}")
    print(f"Number of Hats (D-Pads): {joystick.get_numhats()}")

    # Track previous button states
    previous_button_states = {i: False for i in range(joystick.get_numbuttons())}

    # Track previous axis states (for D-pad movement)
    previous_axis_states = {i: 0 for i in range(joystick.get_numaxes())}

else:
    print("No controller connected!")

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

            # Check if any button is pressed (only print when state changes)
            for button in range(joystick.get_numbuttons()):
                is_pressed = joystick.get_button(button)
                if is_pressed and not previous_button_states[button]:  # Detect new press
                    button_pressed = True
                    if controller_guid in controller_profiles and controller_profiles[controller_guid] == "Buffalo Classic USB Gamepad":
                        button_name = buffalo_button_map.get(button, f"Unknown Button {button}")
                    else:
                        button_name = f"Button {button}"
                    print(f"{button_name} pressed!")

                # Update button state
                previous_button_states[button] = is_pressed

            # Check D-pad via axes (Buffalo controller uses two axes instead of hats)
            for axis in range(joystick.get_numaxes()):
                axis_value = round(joystick.get_axis(axis))  # Round for cleaner output (-1, 0, 1)
                
                # Only print when the axis value CHANGES (prevents repeat spam)
                if axis_value != previous_axis_states[axis]:  
                    if axis_value != 0:  # Ignore resting state
                        button_pressed = True
                        if controller_guid in controller_profiles and controller_profiles[controller_guid] == "Buffalo Classic USB Gamepad":
                            axis_name = buffalo_axis_map.get((axis, axis_value), f"Axis {axis} moved: {axis_value:.2f}")
                        else:
                            axis_name = f"Axis {axis} moved: {axis_value:.2f}"
                        print(axis_name)

                # Update axis state
                previous_axis_states[axis] = axis_value

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
