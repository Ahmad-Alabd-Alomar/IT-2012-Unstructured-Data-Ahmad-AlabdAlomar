from PIL import Image
from PIL.ExifTags import TAGS
import logging

def extract_exif(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            print(f"No EXIF data found in {image_path}")
            return None

        readable_exif = {}
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            readable_exif[tag_name] = str(value)

        print("\n--- EXIF DATA EXTRACTED ---")
        for k, v in list(readable_exif.items())[:15]: 
            print(f"{k}: {v}")
        return readable_exif
    except Exception as e:
        logging.error(f"Failed to extract EXIF: {e}")
        return None