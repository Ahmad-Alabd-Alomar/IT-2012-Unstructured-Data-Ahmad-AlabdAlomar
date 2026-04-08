import os
from PIL import Image, ImageFilter, ImageEnhance
import logging

def process_image(file_path):
    try:
        img = Image.open(file_path)
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)

        # 2. Inspect Properties
        metadata = {
            "file_name": filename,
            "original_size": img.size,
            "mode": img.mode,
            "format": img.format,
            "file_size_bytes": file_size
        }

        # Ensure output directories exist
        os.makedirs("data/processed/resized", exist_ok=True)
        os.makedirs("data/processed/thumbnails", exist_ok=True)
        os.makedirs("data/processed/cropped", exist_ok=True)
        os.makedirs("data/processed/webp", exist_ok=True)
        os.makedirs("data/processed/filtered", exist_ok=True)

        # 3. Resize and Thumbnail
        img.resize((500, 500)).save(f"data/processed/resized/{filename}")
        
        thumb = img.copy()
        thumb.thumbnail((128, 128))
        thumb.save(f"data/processed/thumbnails/{filename}")

        # 4. Crop (Center Square)
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        img.crop((left, top, right, bottom)).save(f"data/processed/cropped/{filename}")

        # 5. Format Conversion (WebP)
        name_only = os.path.splitext(filename)[0]
        img.save(f"data/processed/webp/{name_only}.webp", "WEBP", quality=80)

        # 6. Apply Filters (Blur & Contrast)
        blurred = img.filter(ImageFilter.BLUR)
        enhancer = ImageEnhance.Contrast(blurred)
        enhancer.enhance(1.5).save(f"data/processed/filtered/{filename}")

        return metadata

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        return None