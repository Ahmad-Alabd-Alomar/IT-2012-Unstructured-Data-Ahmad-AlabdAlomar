import json
import logging
from pathlib import Path
from PIL import Image 

def setup_logging(log_file):
    """Sets up a log file to track successes and errors."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def read_json(file_path):
    """Reads course metadata and handles errors if the file is missing or broken."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info(f"Successfully read JSON: {file_path}")
            return data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in: {file_path}")

def read_text(file_path):
    """Reads student reviews or transcripts."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            logging.info(f"Successfully read text file: {file_path}")
            return text
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")



def read_image_metadata(file_path):
    """Reads basic metadata from a course thumbnail image."""
    try:
        with Image.open(file_path) as img:
            logging.info(f"Successfully read image: {file_path}")
            return {"format": img.format, "size": img.size, "mode": img.mode}
    except FileNotFoundError:
        logging.error(f"Image file not found: {file_path}")
    except Exception as e:
        logging.error(f"Error reading image {file_path}: {e}")

def read_transcript(file_path):
    """
    Reads a video transcript (.txt or .srt). 
    In an education pipeline, this is how we 'process' video content.
    """
    return read_text(file_path) # We can reuse our read_text function!