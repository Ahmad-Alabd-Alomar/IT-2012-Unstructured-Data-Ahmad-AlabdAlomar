import os
import pytesseract
from PIL import Image, ImageEnhance
from pdf2image import convert_from_path
import logging

# NOTE FOR WINDOWS USERS: 
# If pytesseract crashes saying "tesseract is not installed", you need to tell Python exactly where it is.
# Uncomment the line below and make sure the path matches where you installed Tesseract:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    """Lab 5 Requirement: Applies preprocessing to improve OCR accuracy."""
    # Convert to grayscale
    gray_image = image.convert('L')
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2.0)
    return enhanced_image

def process_image(image_path):
    """Extracts text from an image, comparing raw vs preprocessed OCR."""
    logging.info(f"Running OCR on image: {image_path}")
    try:
        img = Image.open(image_path)
        
        # 1. Raw OCR
        raw_text = pytesseract.image_to_string(img)
        
        # 2. Preprocessed OCR
        processed_img = preprocess_image(img)
        processed_text = pytesseract.image_to_string(processed_img)
        
        return {
            "raw_text_extracted": raw_text.strip(),
            "preprocessed_text_extracted": processed_text.strip(),
            "preprocessing_improved_results": raw_text != processed_text
        }
    except Exception as e:
        logging.error(f"OCR failed for image {image_path}: {e}")
        return None

def process_scanned_pdf(pdf_path):
    """Lab 5 Requirement: Converts a scanned PDF to images and applies OCR."""
    logging.info(f"Running OCR on scanned PDF: {pdf_path}")
    extracted_pages = []
    try:
        # Note: on Windows, you might need to add poppler_path=r'C:\path\to\poppler\bin' as an argument here
        images = convert_from_path(pdf_path)
        
        for i, img in enumerate(images):
            logging.info(f"Processing page {i+1} of {pdf_path}")
            
            raw_text = pytesseract.image_to_string(img)
            processed_img = preprocess_image(img)
            processed_text = pytesseract.image_to_string(processed_img)
            
            extracted_pages.append({
                "page_number": i + 1,
                "raw_text": raw_text.strip(),
                "preprocessed_text": processed_text.strip()
            })
            
        return extracted_pages
    except Exception as e:
        logging.error(f"OCR failed for scanned PDF {pdf_path}: {e}")
        return None