import os
import shutil
from deepface import DeepFace

def get_age_group(age):
    """Categorize age into 5-year intervals"""
    lower = ((age - 1) // 5) * 5 + 1
    upper = lower + 4
    return f"{lower}-{upper}"

def process_images(input_dir, output_dir):
    """Process images to detect age and organize into folders"""
    image_exts = ('.jpg', '.jpeg', '.png', '.webp')
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(image_exts):
            img_path = os.path.join(input_dir, filename)
            
            try:
                # Detect face and estimate age
                results = DeepFace.analyze(
                    img_path=img_path,
                    actions=['age'],
                    enforce_detection=True,
                    detector_backend='ssd'  # Fast face detection model
                )
            except ValueError as e:
                print(f"Skipping {filename}: No face detected - {str(e)}")
                continue
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue

            # Extract age from results
            age = int(results[0]['age'])
            age_group = get_age_group(age)

            # Create destination folder
            dest_folder = os.path.join(output_dir, age_group)
            os.makedirs(dest_folder, exist_ok=True)

            # Create new filename with age
            base_name, ext = os.path.splitext(filename)
            new_filename = f"{base_name}_{age}{ext}"
            dest_path = os.path.join(dest_folder, new_filename)

            # Move and rename file
            shutil.move(img_path, dest_path)
            print(f"Processed: {filename} → {dest_path}")

if __name__ == "__main__":
    # Configuration
    input_directory = r"C:\Users\ReX\Desktop\Face"       # Folder with input images
    output_directory = r"C:\Users\ReX\Desktop\Organised"     # Main output folder
    
    # Create output directory if needed
    os.makedirs(output_directory, exist_ok=True)
    
    # Start processing
    print("Starting age-based image organization...")
    process_images(input_directory, output_directory)
    print("\nProcessing completed. Check the 'sorted' folder for results.")