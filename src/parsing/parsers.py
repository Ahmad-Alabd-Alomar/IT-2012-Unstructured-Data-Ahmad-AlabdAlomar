import csv
import xml.etree.ElementTree as ET

def extract_course_fields(raw_data):
    """Extracts specific fields from iTunes Education API data."""
    return {
        "course_id": raw_data.get("collectionId"),
        "title": raw_data.get("collectionName"),
        "price": raw_data.get("trackPrice", 0.00),
        "instructor": raw_data.get("artistName", "Unknown"),
        "image_url": raw_data.get("artworkUrl600")
    }

def parse_csv_courses(file_path):
    """Lab 3 Requirement: Parses course data from a CSV file."""
    courses = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                courses.append(row)
        return courses
    except FileNotFoundError:
        return []

def parse_xml_courses(file_path):
    """Lab 3 Requirement: Parses course data from an XML file."""
    courses = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for child in root:
            courses.append(child.attrib)
        return courses
    except FileNotFoundError:
        return []