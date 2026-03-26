import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
import boto3

load_dotenv()

def test_connections():
    print("Checking Vault...")
    
    # 1. Test API
    cid = os.getenv("UDEMY_CLIENT_ID")
    if cid:
        print("✅ Udemy Keys: Found")
    else:
        print("❌ Udemy Keys: MISSING")

    # 2. Test MongoDB
    try:
        client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB: Connected")
    except Exception:
        print("❌ MongoDB: Connection Failed (Is it running?)")

    # 3. Test S3
    try:
        s3 = boto3.client('s3', 
                          aws_access_key_id=os.getenv("AWS_ACCESS_KEY"), 
                          aws_secret_access_key=os.getenv("AWS_SECRET_KEY"))
        s3.list_buckets()
        print("✅ AWS S3: Credentials Valid")
    except Exception:
        print("❌ AWS S3: Connection Failed")

if __name__ == "__main__":
    test_connections()