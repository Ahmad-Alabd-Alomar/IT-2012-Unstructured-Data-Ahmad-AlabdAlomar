import boto3
import os
import logging
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_SECRET_KEY")

def upload_to_s3(local_file_path, s3_file_name):
    """Uploads a local file to LocalStack S3 (Lab 3 requirement)."""
    # Added the LocalStack endpoint and region
    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url='http://localhost:4566',
        region_name='us-east-1' 
    )

    try:
        logging.info(f"Uploading {local_file_path} to S3 bucket {S3_BUCKET}...")
        s3.upload_file(local_file_path, S3_BUCKET, s3_file_name)
        logging.info("Upload Successful!")
        return True
    except FileNotFoundError:
        logging.error("The local file was not found.")
    except NoCredentialsError:
        logging.error("AWS Credentials not found. Check your .env file.")
    except Exception as e:
        logging.error(f"S3 Upload failed: {e}")
        return False