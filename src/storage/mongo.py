from pymongo import MongoClient
import os
import logging

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