# /// script
# requires-python = ">=3.11"
# dependencies = [ "PyYAML" ]
# ///

import os
import json
from pathlib import Path
import yaml

IMAGES_DIR = Path('images')
OUTPUT_FILE = Path('gallery-data.json')
SITE_CONFIG_FILE = Path('site.yaml')
SITE_OUTPUT_FILE = Path('site-data.json')

def parse_collection_prefix(folder_name):
    """
    Parses numeric prefix from folder name.
    Returns (prefix_number, clean_name) or (None, folder_name)
    Example: "2_back_to_the_garden" -> (2, "back_to_the_garden")
    """
    import re
    match = re.match(r'^(\d+)_(.+)$', folder_name)
    if match:
        prefix_num = int(match.group(1))
        clean_name = match.group(2)
        return (prefix_num, clean_name)
    return (None, folder_name)

def collection_sort_key(folder_path):
    """
    Returns sort key: (numeric_prefix or infinity, folder_name)
    Numbered collections sort first, non-numbered last.
    Within same prefix level, sorts alphabetically.
    """
    folder_name = folder_path.name
    prefix, clean_name = parse_collection_prefix(folder_name)
    # Use infinity for non-numbered collections so they sort last
    sort_prefix = prefix if prefix is not None else float('inf')
    return (sort_prefix, clean_name)

def format_collection_name(name):
    """Formats a folder name like 'collection1' into a title like 'Collection 1'."""
    # Strip numeric prefix if present
    _, clean_name = parse_collection_prefix(name)
    return clean_name.replace('_', ' ').replace('-', ' ').title()

def get_existing_data():
    """Loads the existing gallery data if it exists."""
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def run_build():
    """Scans the images directory and generates a JSON data file for the gallery."""
    print("Starting build...")

    # --- Process site config ---
    if SITE_CONFIG_FILE.exists():
        print(f"Processing site config from {SITE_CONFIG_FILE}...")
        with open(SITE_CONFIG_FILE, 'r', encoding='utf-8') as f:
            site_data = yaml.safe_load(f)
        with open(SITE_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(site_data, f, indent=4)
        print(f"Site data written to '{SITE_OUTPUT_FILE}'.")
    else:
        print(f"Warning: '{SITE_CONFIG_FILE}' not found.")

    # --- Process gallery images ---
    existing_data = get_existing_data()
    gallery_data = {}

    if not IMAGES_DIR.exists() or not IMAGES_DIR.is_dir():
        print(f"Error: '{IMAGES_DIR}' directory not found.")
        return

    # Find all collection directories
    collection_dirs = [d for d in IMAGES_DIR.iterdir() if d.is_dir()]

    for collection_dir in sorted(collection_dirs, key=collection_sort_key):
        collection_name_str = collection_dir.name
        collection_title = format_collection_name(collection_name_str)
        print(f"Processing collection: {collection_title}...")

        # Read collection description
        info_file = collection_dir / '_collection.info'
        description = ""
        if info_file.exists():
            with open(info_file, 'r', encoding='utf-8') as f:
                description = f.read().strip()
        
        # Prepare collection data structure
        gallery_data[collection_title] = {
            "description": description,
            "paintings": []
        }

        # Find all image files
        image_files = sorted(list(collection_dir.glob('*.jpg')) + list(collection_dir.glob('*.png')))

        for img_path in image_files:
            img_filename = img_path.name
            relative_path = f"{collection_name_str}/{img_filename}"

            # Check if we have existing data for this image
            existing_painting_data = None
            if collection_title in existing_data and "paintings" in existing_data[collection_title]:
                for p in existing_data[collection_title]["paintings"]:
                    if p.get("file") == relative_path:
                        existing_painting_data = p
                        break
            
            if existing_painting_data:
                # Preserve existing data
                gallery_data[collection_title]["paintings"].append(existing_painting_data)
            else:
                # Add new image with placeholder data
                print(f"  Adding new image: {img_filename}")
                gallery_data[collection_title]["paintings"].append({
                    "file": relative_path,
                    "title": f"{img_path.stem.replace('_', ' ').replace('-', ' ').title()}",
                    "meta": "Medium, Size",
                    "price": "$TBD"
                })

    # Write the new data file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(gallery_data, f, indent=4, ensure_ascii=False)
    
    print(f"\nBuild complete. Gallery data written to '{OUTPUT_FILE}'.")
    print("You can now edit this file to update painting details.")

if __name__ == '__main__':
    run_build()
