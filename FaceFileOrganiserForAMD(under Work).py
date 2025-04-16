import os
import cv2
import shutil
from concurrent.futures import ProcessPoolExecutor
from deepface import DeepFace

# Configuration
INPUT_DIR = r""  # Notice the 'r' before the string
OUTPUT_DIR = r""  # Apply to all Windows paths
IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.webp')
MAX_WIDTH = 640  # Resize larger images for faster processing
DETECTOR_BACKEND = 'opencv'  # Fastest CPU-based detector

def get_age_group(age):
    """Categorize age into 5-year intervals"""
    lower = ((age - 1) // 5) * 5 + 1
    return f"{lower}-{lower+4}"

def process_single_image(filename):
    """Process individual image with optimized settings"""
    try:
        img_path = os.path.join(INPUT_DIR, filename)
        
        # Read and preprocess image
        img = cv2.imread(img_path)
        if img is None:
            return (filename, None, "Invalid image file")
            
        # Resize large images while maintaining aspect ratio
        h, w = img.shape[:2]
        if w > MAX_WIDTH:
            ratio = MAX_WIDTH / w
            img = cv2.resize(img, (MAX_WIDTH, int(h * ratio)))

        # Convert to RGB and analyze
        results = DeepFace.analyze(
            img=img,
            actions=['age'],
            enforce_detection=True,
            detector_backend=DETECTOR_BACKEND,
            silent=True  # Disable unnecessary logging
        )

        return (filename, int(results[0]['age']), None)
        
    except Exception as e:
        return (filename, None, str(e))

def organize_results(results):
    """Move files to appropriate directories after processing"""
    for filename, age, error in results:
        if error:
            print(f"Skipped {filename}: {error}")
            continue
            
        src_path = os.path.join(INPUT_DIR, filename)
        age_group = get_age_group(age)
        dest_dir = os.path.join(OUTPUT_DIR, age_group)
        
        os.makedirs(dest_dir, exist_ok=True)
        
        new_name = f"{os.path.splitext(filename)[0]}_{age}{os.path.splitext(filename)[1]}"
        dest_path = os.path.join(dest_dir, new_name)
        
        shutil.move(src_path, dest_path)
        print(f"Moved {filename} → {dest_path}")

if __name__ == "__main__":
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get image list
    image_files = [f for f in os.listdir(INPUT_DIR) 
                 if f.lower().endswith(IMAGE_EXTS)]
    
    print(f"Found {len(image_files)} images to process")
    print("Starting parallel processing...")

    # Use ProcessPoolExecutor for CPU-bound tasks
    with ProcessPoolExecutor(max_workers=6) as executor:  # 6 cores for 5600G
        results = list(executor.map(process_single_image, image_files))

    print("\nProcessing complete. Organizing files...")
    organize_results(results)
    print("Done!")
