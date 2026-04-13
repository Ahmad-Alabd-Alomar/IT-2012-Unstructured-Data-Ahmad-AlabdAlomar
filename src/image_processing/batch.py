import os
from tqdm import tqdm
import logging
from src.image_processing.processor import process_image
from src.storage.mongo import save_to_mongo
from src.utils.upload_utils import upload_batch

def batch_process_images(image_paths):
    logging.info(f"Starting batch processing of {len(image_paths)} images...")
    processed_metadata = []
    webp_paths_to_upload = []

    # tqdm creates the progress bar
    for path in tqdm(image_paths, desc="Processing Images"):
        metadata = process_image(path)
        if metadata:
            processed_metadata.append(metadata)
            name_only = os.path.splitext(os.path.basename(path))[0]
            webp_paths_to_upload.append(f"data/processed/webp/{name_only}.webp")

    # Save metadata to MongoDB
    if processed_metadata:
        save_to_mongo(processed_metadata, "processed_image_metadata")

    # Upload ONLY the first 10 WebP versions to Drive (saves bandwidth/time)
    if webp_paths_to_upload:
        logging.info("Starting Google Drive upload...")
        upload_batch(webp_paths_to_upload[:10]) 

    logging.info("Batch processing and upload complete.")