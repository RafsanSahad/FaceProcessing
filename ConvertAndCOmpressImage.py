import os
import sys
from PIL import Image
from pillow_heif import register_heif_opener
import xattr  # For handling macOS extended attributes

# Configuration
INPUT_DIR = "/Volumes/Disk 1 main/HED/Angry"
OUTPUT_DIR = "/Volumes/Disk 1 main/Head Compress"
COMPRESSION_QUALITY = 60

def is_hidden_macos_file(filename):
    """Check if file is a macOS hidden file"""
    return filename.startswith('.') or filename == 'DS_Store'

def clean_macos_attributes(filepath):
    """Remove macOS extended attributes if they exist"""
    try:
        attrs = xattr.listxattr(filepath)
        for attr in attrs:
            if not attr.startswith('com.apple.FinderInfo'):
                xattr.removexattr(filepath, attr)
    except:
        pass

def process_images():
    register_heif_opener()
    supported_exts = ('.jpg', '.jpeg', '.png', '.webp', '.heic')
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"🔍 Scanning {INPUT_DIR} for images...")
    
    try:
        files = [f for f in os.listdir(INPUT_DIR) 
                if f.lower().endswith(supported_exts) 
                and not is_hidden_macos_file(f)]
    except FileNotFoundError:
        print(f"❌ Error: Directory not found - {INPUT_DIR}")
        print("Please check:")
        print(f"1. Is the drive mounted? (Current volumes: {os.listdir('/Volumes')})")
        print("2. Is the path correct?")
        return
    
    if not files:
        print("❌ No supported images found")
        return
    
    print(f"Found {len(files)} images to process")
    
    for i, filename in enumerate(files, 1):
        input_path = os.path.join(INPUT_DIR, filename)
        output_filename = f"{os.path.splitext(filename)[0]}.jpg"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        print(f"\n{i}/{len(files)} Processing {filename}")
        
        try:
            # Clean macOS attributes before processing
            clean_macos_attributes(input_path)
            
            # Convert and compress in one step
            with Image.open(input_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, "JPEG", 
                       quality=COMPRESSION_QUALITY, 
                       optimize=True)
            
            print(f"✅ Saved to {output_path}")
            
        except Exception as e:
            print(f"❌ Failed to process {filename}: {str(e)}")

if __name__ == "__main__":
    try:
        import xattr
    except ImportError:
        print("⚠️  Install xattr for better macOS support: pip install xattr")
    
    print("\n🖼️  macOS Image Processor")
    print("="*40)
    process_images()
    print("\n" + "="*40)
    print("✨ All done!")