from pymongo import MongoClient
import os
import logging
from datetime import datetime

def save_to_mongo(data, collection_name):
    """Saves parsed data to the local MongoDB database."""
    try:
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client[os.getenv("DB_NAME")]
        collection = db[collection_name]
        
        # Don't try to insert an empty list
        if isinstance(data, list) and len(data) > 0:
            collection.insert_many(data)
        elif isinstance(data, dict):
            collection.insert_one(data)
            
        logging.info(f"Successfully saved data to MongoDB collection: {collection_name}")
    except Exception as e:
        logging.error(f"Failed to save to MongoDB: {e}")

def save_transcript(transcript_result, collection_name="transcripts"):
    """Lab 7: Saves transcription data with timestamps and metadata to MongoDB."""
    try:
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client[os.getenv("DB_NAME")]
        collection = db[collection_name]
        
        doc = {
            'source_file': transcript_result.get('source_file', ''),
            'source_path': transcript_result.get('source_path', ''),
            'model': transcript_result.get('model', 'unknown'),
            'language': transcript_result.get('language', ''),
            'duration_s': transcript_result.get('duration_s', 0),
            'full_text': transcript_result.get('full_text', ''),
            'segments': transcript_result.get('segments', []),
            'transcribed_at': datetime.utcnow().isoformat(),
        }
        collection.insert_one(doc)
        logging.info(f"Successfully saved transcript for {doc['source_file']} to MongoDB.")
    except Exception as e:
        logging.error(f"Failed to save transcript to MongoDB: {e}")