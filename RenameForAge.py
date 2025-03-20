import os
import cv2
import shutil
from deepface import DeepFace
from pillow_heif import register_heif_opener  # For HEIC support
from PIL import Image  # For image conversion

# Configuration
INPUT_DIR = "Face"  # Folder containing original images
OUTPUT_DIR = "RenameForAge"  # Folder to save renamed images
IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.heic')  # Supported input formats
MAX_WIDTH = 640  # Resize limit
DETECTOR_BACKEND = 'opencv'

# Enable HEIC support
register_heif_opener()

# Ensure Output Directory Exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_heic_to_jpg(heic_path, jpg_path):
    """Convert HEIC image to JPEG"""
    try:
        img = Image.open(heic_path)
        img.convert("RGB").save(jpg_path, "JPEG")
        return True
    except Exception as e:
        print(f"Error converting {heic_path} to JPEG: {e}")
        return False

def process_single_image(filename):
    """Process individual image"""
    try:
        img_path = os.path.join(INPUT_DIR, filename)
        temp_path = None

        # Convert HEIC to JPEG if necessary
        if filename.lower().endswith('.heic'):
            temp_path = os.path.join(INPUT_DIR, f"{os.path.splitext(filename)[0]}.jpg")
            if not convert_heic_to_jpg(img_path, temp_path):
                return (filename, None, "HEIC conversion failed")
            img_path = temp_path  # Use the converted JPEG file

        # Read the image
        img = cv2.imread(img_path)

        if img is None:
            print(f"Unable to read {filename}. It may be corrupted or unsupported.")
            return (filename, None, "Invalid image file")
        
        # Convert BGR to RGB (DeepFace expects RGB images)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Resize if needed
        h, w = img.shape[:2]
        if w > MAX_WIDTH:
            ratio = MAX_WIDTH / w
            img = cv2.resize(img, (MAX_WIDTH, int(h * ratio)))

        # Analyze Age
        results = DeepFace.analyze(
            img_path=img_path,  # Pass the file path
            actions=['age'],
            enforce_detection=False,  # Set to True if you want to enforce face detection
            detector_backend=DETECTOR_BACKEND,
            silent=True
        )

        # Extract age from results
        age = float(results[0]['age'])
        return (filename, age, None)

    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return (filename, None, str(e))
    finally:
        # Clean up temporary JPEG file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

def rename_and_save_images():
    """Rename images based on detected age and save to RenameForAge folder"""
    age_count = {}  # Track how many times each age has been used

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(IMAGE_EXTS):
            result = process_single_image(filename)
            filename, age, error = result

            if error:
                print(f"Skipped {filename}: {error}")
                continue

            # Create a base name for the file (e.g., "image32")
            base_name = f"image{int(age)}"

            # Check if this base name has been used before
            if base_name not in age_count:
                age_count[base_name] = 0
                new_name = f"{base_name}{os.path.splitext(filename)[1]}"
            else:
                age_count[base_name] += 1
                new_name = f"{base_name}_{age_count[base_name]}{os.path.splitext(filename)[1]}"

            # Save the renamed file to the RenameForAge folder
            src_path = os.path.join(INPUT_DIR, filename)
            dest_path = os.path.join(OUTPUT_DIR, new_name)
            shutil.copy(src_path, dest_path)
            print(f"Renamed and saved {filename} → {dest_path}")

# Rename and Save Images
rename_and_save_images()

print("\nProcess complete. Images renamed and saved to the RenameForAge folder.")