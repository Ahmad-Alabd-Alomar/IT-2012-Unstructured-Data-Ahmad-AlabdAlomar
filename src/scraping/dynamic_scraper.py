from playwright.sync_api import sync_playwright
import logging

def scrape_dynamic_quotes():
    """Lab 5 Requirement: Dynamic Content Handling using Playwright."""
    target_url = "http://quotes.toscrape.com/js/"
    extracted_quotes = []

    logging.info(f"Starting Playwright dynamic scraper for: {target_url}")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(target_url)
            
            page.wait_for_selector(".quote")
            
            # Extract data
            quotes = page.query_selector_all(".quote")
            for quote in quotes:
                text = quote.query_selector(".text").inner_text()
                author = quote.query_selector(".author").inner_text()
                extracted_quotes.append({
                    "quote": text,
                    "author": author,
                    "source_url": target_url,
                    "is_dynamic": True
                })
                
            browser.close()
    except Exception as e:
        logging.error(f"Dynamic scraping failed: {e}")
        
    return extracted_quotes