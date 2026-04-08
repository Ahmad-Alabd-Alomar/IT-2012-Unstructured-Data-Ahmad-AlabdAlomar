import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from src.api.client import fetch_udemy_courses
from src.parsing.parsers import extract_course_fields
from src.storage.mongo import save_to_mongo
from src.storage.s3 import upload_to_s3
from src.utils.io_utils import setup_logging  
from src.parsing.doc_parsers import extract_from_pdf, extract_from_word, extract_from_excel
from src.scraping.scraper import scrape_books_catalog
from src.scraping.dynamic_scraper import scrape_dynamic_quotes
from src.ocr.ocr_utils import process_image, process_scanned_pdf

load_dotenv()

# --- LAB 3: API Pipeline ---
def process_api_data():
    logging.info("--- Starting API Data Pipeline ---")
    topic = "Python"
    all_raw_data = []
    
    for page in range(1, 4):
        page_data = fetch_udemy_courses(search_term=topic, page=page)
        all_raw_data.extend(page_data)
    
    if not all_raw_data: return

    for raw_course in all_raw_data:
        cleaned = extract_course_fields(raw_course)
        save_to_mongo(cleaned, "online_courses")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_filename = f"data/raw/api/courses_{timestamp}.json"
    os.makedirs(os.path.dirname(local_filename), exist_ok=True)
    with open(local_filename, "w", encoding="utf-8") as f:
        json.dump(all_raw_data, f, indent=4)
    upload_to_s3(local_filename, f"backups/raw_api_data/courses_{timestamp}.json")

# --- LAB 4: Document Pipeline ---
def process_local_documents():
    logging.info("--- Starting Document Extraction Pipeline ---")
    doc_processors = {"pdf": extract_from_pdf, "word": extract_from_word, "excel": extract_from_excel}
    base_dir = "data/raw"
    
    for doc_type, parser_func in doc_processors.items():
        folder_path = os.path.join(base_dir, doc_type)
        if not os.path.exists(folder_path): continue
            
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                logging.info(f"Extracting data from: {filename}")
                extracted_content = parser_func(file_path)
                if extracted_content:
                    document_record = {
                        "file_name": filename,
                        "document_type": doc_type.upper(),
                        "extraction_timestamp": datetime.now().isoformat(),
                        "source": f"local_directory/{doc_type}",
                        "content": extracted_content
                    }
                    save_to_mongo(document_record, "extracted_documents")

# --- LAB 5: Web Scraping Pipeline ---
def process_web_scraping():
    logging.info("--- Starting Web Scraping Pipeline ---")
    
    # 1. Static Scraping (BeautifulSoup)
    static_data = scrape_books_catalog(max_pages=2)
    if static_data:
        scrape_record = {
            "file_name": "books.toscrape.com",
            "type": "STATIC_HTML",
            "timestamp": datetime.now().isoformat(),
            "source": "Web Scraper",
            "content": static_data
        }
        save_to_mongo(scrape_record, "web_scraped_data")

    # 2. Dynamic Scraping (Playwright)
    dynamic_data = scrape_dynamic_quotes()
    if dynamic_data:
        dynamic_record = {
            "file_name": "quotes.toscrape.com",
            "type": "DYNAMIC_JS",
            "timestamp": datetime.now().isoformat(),
            "source": "Playwright Scraper",
            "content": dynamic_data
        }
        save_to_mongo(dynamic_record, "web_scraped_data")

# --- LAB 5: OCR Pipeline ---
def process_ocr():
    logging.info("--- Starting OCR Processing Pipeline ---")
    
    # Process Images
    img_dir = "data/raw/images"
    if os.path.exists(img_dir):
        for filename in os.listdir(img_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                result = process_image(os.path.join(img_dir, filename))
                if result:
                    ocr_record = {
                        "file_name": filename,
                        "type": "OCR_IMAGE",
                        "timestamp": datetime.now().isoformat(),
                        "source": "Tesseract",
                        "content": result
                    }
                    save_to_mongo(ocr_record, "ocr_data")

    # Process Scanned PDFs
    pdf_dir = "data/raw/scanned"
    if os.path.exists(pdf_dir):
        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith('.pdf'):
                result = process_scanned_pdf(os.path.join(pdf_dir, filename))
                if result:
                    ocr_record = {
                        "file_name": filename,
                        "type": "OCR_PDF",
                        "timestamp": datetime.now().isoformat(),
                        "source": "Tesseract + Poppler",
                        "content": result
                    }
                    save_to_mongo(ocr_record, "ocr_data")

def run_pipeline():
    """Main Orchestrator: Runs Lab 3, 4, and 5 sequentially."""
    setup_logging("pipeline_run.log")
    print("🚀 Pipeline started! Check pipeline_run.log for real-time progress.")
    
    try:
        process_api_data()
        process_local_documents()
        process_web_scraping()
        process_ocr()
        print("✅ Pipeline complete! API, Documents, Web Scraping, and OCR data stored.")
    except Exception as e:
        logging.error(f"Pipeline crashed: {e}")
        print("❌ Pipeline failed. Check the logs.")

if __name__ == "__main__":
    run_pipeline()