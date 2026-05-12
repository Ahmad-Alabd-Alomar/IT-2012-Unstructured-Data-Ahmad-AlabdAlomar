from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv
import logging

load_dotenv()

def run_mongo_aggregation():
    """Executes a 4-stage MongoDB aggregation pipeline natively in the database."""
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("DB_NAME")]
    collection = db["online_courses"]
    
    pipeline = [
        # Stage 1: Match documents that have an instructor
        {"$match": {"instructor": {"$exists": True, "$ne": None}}}, 
        
        # Stage 2: Convert price to string safely
        {"$project": { 
            "instructor": 1,
            "price_string": {"$toString": "$price"} 
        }},
        
        # Stage 3: Remove the literal '$' symbol
        {"$project": {
            "instructor": 1,
            "price_clean": {"$replaceAll": {"input": "$price_string", "find": {"$literal": "$"}, "replacement": ""}}
        }},
        
        # Stage 4: Convert clean string to double safely
        {"$project": {
            "instructor": 1,
            "price_numeric": {"$convert": {"input": "$price_clean", "to": "double", "onError": 19.99, "onNull": 19.99}}
        }},
        
        # Stage 5: Group by Instructor
        {"$group": { 
            "_id": "$instructor",
            "avg_price": {"$avg": "$price_numeric"},
            "course_count": {"$sum": 1}
        }},
        
        # Stage 6: Sort by course count (highest first)
        {"$sort": {"course_count": -1}} 
    ]
    
    try:
        result = list(collection.aggregate(pipeline))
        df = pd.DataFrame(result)
        if not df.empty:
            df.rename(columns={"_id": "instructor"}, inplace=True)
            logging.info("MongoDB aggregation pipeline executed successfully.")
            return df
    except Exception as e:
        logging.error(f"MongoDB Aggregation failed: {e}")
        
    return pd.DataFrame()