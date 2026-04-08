import requests
import logging

def fetch_udemy_courses(search_term="Python", page=1):
    """Fallback: Fetches educational courses from iTunes API (No auth required)."""
    url = "https://itunes.apple.com/search"
    

    offset = (page - 1) * 10
    
    params = {
        "term": search_term,
        "entity": "podcast", 
        "limit": 10,
        "offset": offset
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            logging.info(f"Successfully fetched iTunes page {page}")
            return response.json().get("results", [])
        else:
            logging.error(f"API Error {response.status_code}: {response.text}")
            return []
    except Exception as e:
        logging.error(f"Failed to connect to iTunes API: {e}")
        return []

# --- Quick Test Block ---
if __name__ == "__main__":
    print("Testing iTunes API Connection...")
    courses = fetch_udemy_courses(search_term="Python", page=1)
    if courses:
        print(f"✅ Success! Found {len(courses)} courses.")
        print(f"Sample Title: {courses[0].get('collectionName', 'Unknown')}")
        print(f"Sample Image URL: {courses[0].get('artworkUrl600', 'No Image')}")
    else:
        print("❌ Failed to fetch courses.")