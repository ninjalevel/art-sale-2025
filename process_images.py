# /// script
# dependencies = [
#   "Pillow",
# ]
# ///

import os
from PIL import Image, ImageOps
import glob

def resize_images():
    """
    Resizes all JPG images from an input directory to a max width of 1200px,
    maintaining aspect ratio, and saves them to an output directory.
    """
    input_dir = 'images_raw'
    output_dir = 'images'
    max_width = 1200

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Find all JPG files in the input directory
    image_paths = glob.glob(os.path.join(input_dir, '*.jpg'))
    
    if not image_paths:
        print(f"No JPG images found in '{input_dir}'.")
        return

    print(f"Found {len(image_paths)} images to process...")

    for img_path in image_paths:
        try:
            with Image.open(img_path) as img:
                # Correct the orientation based on EXIF data
                img = ImageOps.exif_transpose(img)

                # Calculate new height to maintain aspect ratio
                width_percent = (max_width / float(img.size[0]))
                new_height = int((float(img.size[1]) * float(width_percent)))
                
                # Resize the image using a high-quality filter
                img_resized = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Get the original filename
                filename = os.path.basename(img_path)
                
                # Save the resized image to the output directory
                output_path = os.path.join(output_dir, filename)
                img_resized.save(output_path, 'JPEG', quality=85, optimize=True)
                
                print(f"Processed and saved: {output_path}")

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

if __name__ == '__main__':
    resize_images()