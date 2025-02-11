from PIL import Image
import os

def convert_webp_to_jpg(quality=85):
    # Get the directory where the script is running
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Loop through all files in the directory
    for filename in os.listdir(script_dir):
        if filename.lower().endswith(".webp"):
            input_path = os.path.join(script_dir, filename)
            output_path = os.path.join(script_dir, f"{os.path.splitext(filename)[0]}.jpg")
            
            # Check if the JPEG already exists
            if os.path.exists(output_path):
                print(f"Skipping '{filename}' because '{output_path}' already exists.")
                # Remove the original WebP since we assume it’s already been converted
                os.remove(input_path)
                print(f"Removed original WebP file: '{filename}'")
                continue
            
            try:
                # Open the WebP image
                with Image.open(input_path) as img:
                    # Convert and save as JPEG
                    img = img.convert("RGB")
                    img.save(output_path, "JPEG", quality=quality)
                print(f"Converted '{filename}' to '{output_path}' at {quality}% quality.")
                
                # Remove the original WebP file after successful conversion
                os.remove(input_path)
                print(f"Removed original WebP file: '{filename}'")
            except Exception as e:
                print(f"Error converting {filename}: {e}")

# Run the conversion
convert_webp_to_jpg()
