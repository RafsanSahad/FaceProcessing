import os
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Configuration
OUTPUT_DIR = "/content/drive/MyDrive/Organised"  # Folder to create age range subfolders

# Define age ranges (e.g., 11-15, 16-20, etc.)
AGE_RANGES = [
    "age0-5", "age6-10", "age11-15", "age16-20",
    "age21-25", "age26-30", "age31-35", "age36-40",
    "age41-45", "age46-50", "age51-55", "age56-60",
    "age61-65", "age66-70", "age71-75", "age76-80",
    "age81-85", "age86-90", "age91-95", "age96-100"
]

# Ensure Output Directory Exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create age range folders
for age_range in AGE_RANGES:
    age_folder = os.path.join(OUTPUT_DIR, age_range)
    os.makedirs(age_folder, exist_ok=True)
    print(f"Created folder: {age_folder}")

print("\nFolder structure created successfully!")