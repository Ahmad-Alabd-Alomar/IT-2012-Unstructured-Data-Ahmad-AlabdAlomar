import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Importing custom modules
from src.api.client import fetch_udemy_courses
from src.parsing.parsers import extract_course_fields
from src.storage.mongo import save_to_mongo
from src.storage.s3 import upload_to_s3
from src.utils.io_utils import setup_logging  

# NEW: Importing Lab 4 Document Parsers
from src.parsing.doc_parsers import extract_from_pdf, extract_from_word, extract_from_excel

# Load environment variables
load_dotenv()

def process_api_data():
    """Lab 3: Fetches API data and stores it."""
    logging.info("--- Starting API Data Pipeline ---")
    topic = "Python"
    pages_to_fetch = 3
    all_raw_data = []
    
    for page in range(1, pages_to_fetch + 1):
        page_data = fetch_udemy_courses(search_term=topic, page=page)
        all_raw_data.extend(page_data)
    
    if not all_raw_data:
        logging.warning("No API data fetched.")
        return

    logging.info(f"Processing {len(all_raw_data)} API courses...")
    for raw_course in all_raw_data:
        cleaned = extract_course_fields(raw_course)
        save_to_mongo(cleaned, "online_courses")

    # Cloud Backup (S3)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_filename = f"data/raw/api/courses_{timestamp}.json"
    os.makedirs(os.path.dirname(local_filename), exist_ok=True)
    
    with open(local_filename, "w", encoding="utf-8") as f:
        json.dump(all_raw_data, f, indent=4)
    
    upload_to_s3(local_filename, f"backups/raw_api_data/courses_{timestamp}.json")

def process_local_documents():
    """Lab 4: Extracts data from local PDF, Word, and Excel files with Metadata."""
    logging.info("--- Starting Document Extraction Pipeline ---")
    
    # Map the folder names to the specific parser functions
    doc_processors = {
        "pdf": extract_from_pdf,
        "word": extract_from_word,
        "excel": extract_from_excel
    }
    
    base_dir = "data/raw"
    
    for doc_type, parser_func in doc_processors.items():
        folder_path = os.path.join(base_dir, doc_type)
        
        # Skip if the folder doesn't exist yet
        if not os.path.exists(folder_path):
            continue
            
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Only process actual files
            if os.path.isfile(file_path):
                logging.info(f"Extracting data from: {filename}")
                
                # Call the specific parser (PDF, Word, or Excel)
                extracted_content = parser_func(file_path)
                
                if extracted_content:
                    # Lab 4 Requirement: Create the Metadata Wrapper
                    document_record = {
                        "file_name": filename,
                        "document_type": doc_type.upper(),
                        "extraction_timestamp": datetime.now().isoformat(),
                        "source": f"local_directory/{doc_type}",
                        "content": extracted_content
                    }
                    
                    # Save to a NEW collection in MongoDB
                    save_to_mongo(document_record, "extracted_documents")
                    logging.info(f"Successfully saved {filename} with metadata to MongoDB.")
                else:
                    logging.warning(f"Failed to extract content from {filename}")

def run_pipeline():
    """Main Orchestrator: Runs Lab 3 and Lab 4 sequentially."""
    setup_logging("pipeline_run.log")
    print("🚀 Pipeline started! Check pipeline_run.log for real-time progress.")
    
    try:
        process_api_data()
        process_local_documents()
        print("✅ Pipeline complete! All API and Document data processed and stored.")
    except Exception as e:
        logging.error(f"Pipeline crashed: {e}")
        print("❌ Pipeline failed. Check the logs.")

if __name__ == "__main__":
    run_pipeline()