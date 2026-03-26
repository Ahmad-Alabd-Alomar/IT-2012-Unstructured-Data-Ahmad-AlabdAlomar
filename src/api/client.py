import requests

def fetch_udemy_courses(search_term="Python", page=1):
    """Fallback: Fetches educational courses from iTunes API (No auth required)."""
    url = "https://itunes.apple.com/search"
    
    # iTunes uses 'offset' instead of 'page', so we calculate it (10 items per page)
    offset = (page - 1) * 10
    
    params = {
        "term": search_term,
        "entity": "podcast", # Educational podcasts/courses
        "limit": 10,
        "offset": offset
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"API Error {response.status_code}: {response.text}")
        return []