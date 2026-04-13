import os
import requests
import logging
from src.api.client import fetch_udemy_courses

def download_images(limit=100):
    logging.info("Fetching fresh API data to get Image URLs...")
    
    # 1. Grab raw data directly from the iTunes API
    raw_courses = []
    for page in range(1, 4):
        raw_courses.extend(fetch_udemy_courses(search_term="Python", page=page))

    downloaded_paths = []
    save_dir = "data/raw/images"
    os.makedirs(save_dir, exist_ok=True)

    # 2. Extract URLs and Download
    for i, course in enumerate(raw_courses[:limit]):
        url = course.get("artworkUrl600")
        if not url:
            continue

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                file_path = os.path.join(save_dir, f"course_img_{i}.jpg")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                downloaded_paths.append(file_path)
                logging.info(f"Downloaded: {file_path}")
        except Exception as e:
            logging.error(f"Failed to download {url}: {e}")

    return downloaded_paths