import time
import urllib.robotparser
import logging

USER_AGENT = "IT2012_DataPipelineBot/1.0 (Student Project)"

def can_fetch(url, site_url):
    """Lab 5 Requirement: Checks robots.txt before scraping."""
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{site_url}/robots.txt")
    try:
        rp.read()
        return rp.can_fetch(USER_AGENT, url)
    except Exception as e:
        logging.warning(f"Could not read robots.txt for {site_url}: {e}")
        return True # Default to True if robots.txt is missing

def respectful_delay(seconds=2):
    """Lab 5 Requirement: Applies delays between requests."""
    logging.info(f"Sleeping for {seconds} seconds to respect server limits...")
    time.sleep(seconds)