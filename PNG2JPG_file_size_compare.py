# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 09:46:01 2024

@author: Shane
"""

from PIL import Image
import os

def convert_png_to_jpg(quality=85):
    current_directory = os.getcwd()  # Get the current directory where the script is running
    
    # Go through all PNG files in the current directory
    for file_name in os.listdir(current_directory):
        if file_name.lower().endswith(".png"):
            base_name = os.path.splitext(file_name)[0]  # Get the base name without extension
            output_file_name = f"{base_name}.jpg"  # Initial JPG file name
            counter = 1  # Initialize the counter here to prevent uninitialized variable errors

            # Load the PNG image
            try:
                img = Image.open(file_name)
                img = img.convert("RGB")  # Convert to RGB (because JPG doesn't support transparency)
                
                # Temporarily save the new JPG to a unique name for comparison purposes
                temp_output_file = f"{base_name}_temp.jpg"
                img.save(temp_output_file, "JPEG", quality=quality)

                # Check if the target JPG already exists
                if os.path.exists(output_file_name):
                    # Compare file sizes
                    existing_jpg_size = os.path.getsize(output_file_name)
                    new_jpg_size = os.path.getsize(temp_output_file)

                    if new_jpg_size == existing_jpg_size:
                        print(f"{output_file_name} already exists with identical size, skipping...")
                        os.remove(temp_output_file)  # Remove temporary JPG
                        continue  # Skip this file
                    else:
                        # If sizes differ, proceed to rename with a suffix
                        while os.path.exists(output_file_name):
                            output_file_name = f"{base_name}_{counter}.jpg"
                            counter += 1
                            # Avoid infinite loops
                            if counter > 100:
                                print(f"Unable to rename {file_name}, skipping after 100 attempts.")
                                os.remove(temp_output_file)  # Clean up temp file
                                break

                # If we are not skipping, move the temp file to the correct name
                if counter <= 100:
                    os.rename(temp_output_file, output_file_name)  # Rename the temp file
                    print(f"Converted and saved: {file_name} to {output_file_name} with quality: {quality}")
                    
                    # Delete the original PNG file after successful conversion
                    os.remove(file_name)
                    print(f"Deleted original PNG file: {file_name}")
                else:
                    os.remove(temp_output_file)  # Clean up if renaming failed

            except Exception as e:
                print(f"Error converting {file_name}: {e}")

# Call the function
convert_png_to_jpg(quality=85)
