import os
import shutil
from pillow_heif import register_heif_opener  # For HEIC support
from PIL import Image  # For image conversion

# Configuration
INPUT_DIR = "F:\CSE\Face"  # Folder containing original images (relative path)
OUTPUT_DIR = "F:\CSE\FaceConverted"  # Folder to save converted images (relative path)
SUPPORTED_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.heic')  # Supported input formats
OUTPUT_EXT = '.jpg'  # Convert all images to JPEG

# Enable HEIC support
register_heif_opener()

# Ensure Output Directory Exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_image(input_path, output_path):
    """Convert an image to the desired format (JPEG)"""
    try:
        # Open the image
        img = Image.open(input_path)

        # Convert to RGB (if necessary) and save as JPEG
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(output_path, "JPEG")
        print(f"Converted {os.path.basename(input_path)} → {os.path.basename(output_path)}")
        return True
    except Exception as e:
        print(f"Error converting {os.path.basename(input_path)}: {e}")
        return False

def convert_images_in_folder():
    """Convert all images in the input folder to the desired format"""
    for filename in os.listdir(INPUT_DIR):
        # Check if the file has a supported extension
        if filename.lower().endswith(SUPPORTED_EXTS):
            input_path = os.path.join(INPUT_DIR, filename)
            output_filename = f"{os.path.splitext(filename)[0]}{OUTPUT_EXT}"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            # Convert the image
            convert_image(input_path, output_path)

# Convert Images
convert_images_in_folder()

print("\nProcess complete. Images converted and saved to the ConvertedForAge folder.")
