import requests
from bs4 import BeautifulSoup
import logging
from .robots_utils import can_fetch, respectful_delay, USER_AGENT

BASE_URL = "http://books.toscrape.com"

def scrape_books_catalog(max_pages=2):
    """Lab 5 Requirement: Multi-page HTML scraping with BeautifulSoup."""
    scraped_data = []
    headers = {"User-Agent": USER_AGENT}

    if not can_fetch(BASE_URL, BASE_URL):
        logging.error("Scraping forbidden by robots.txt")
        return scraped_data

    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/catalogue/page-{page}.html"
        logging.info(f"Scraping static page {page}: {url}")
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Failed to fetch {url}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            availability = book.find("p", class_="instock availability").text.strip()
            
            scraped_data.append({
                "title": title,
                "price": price,
                "availability": availability,
                "source_url": url
            })

        respectful_delay(1) # Be nice to the server

    return scraped_data