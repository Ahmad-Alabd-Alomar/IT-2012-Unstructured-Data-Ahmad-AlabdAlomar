from utils.io_utils import read_json, setup_logging, read_text
from utils.io_utils import read_json, setup_logging, read_text, read_image_metadata

if __name__ == "__main__":
    # 1. Initialize the log file
    setup_logging("education_pipeline.log")
    
    # 2. Define education data paths
    course_path = "data/raw/courses/course_101.json"
    feedback_path = "data/raw/student_reviews/feedback_1.txt"
    
    # 3. Load and display the data
    course_data = read_json(course_path)
    review_text = read_text(feedback_path)
    
    if course_data:
        print(f"Course Title: {course_data.get('title')}")
        print(f"Instructor: {course_data.get('instructor')}")
        
    if review_text:
        print("\nStudent Feedback (First 100 chars):")
        print(review_text[:100] + "...")

if __name__ == "__main__":
    setup_logging("education_pipeline.log")
    
    # Paths to different data types
    course_path = "data/raw/courses/course_101.json"
    feedback_path = "data/raw/student_reviews/feedback_1.txt"
    thumbnail_path = "data/raw/thumbnails/python_course.png" # You'll need a sample image here
    
    # 1. Load JSON
    course_data = read_json(course_path)
    
    # 2. Load Text/Video Transcript
    review_text = read_text(feedback_path)
    
    # 3. Load Image Metadata
    image_data = read_image_metadata(thumbnail_path)
    
    # Display Results
    if course_data:
        print(f"Course: {course_data.get('title')}")
    if image_data:
        print(f"Thumbnail Dimensions: {image_data['size']}")