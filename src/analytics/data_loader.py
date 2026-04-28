import os
import pandas as pd
import logging
from pymongo import MongoClient

def load_mongo_to_csv(collection_name="online_courses", export_path="data/raw/analytics_export.csv"):
    """Lab 8: Pulls data from MongoDB and exports to a raw CSV."""
    logging.info(f"Extracting {collection_name} from MongoDB to CSV...")
    try:
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client[os.getenv("DB_NAME")]
        
        cursor = db[collection_name].find({}, {"_id": 0})
        df = pd.DataFrame(list(cursor))
        
        if df.empty:
            logging.warning(f"Collection {collection_name} is empty.")
            return None
            
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        df.to_csv(export_path, index=False)
        logging.info(f"Exported {len(df)} records to {export_path}")
        return export_path
    except Exception as e:
        logging.error(f"Failed to export MongoDB data: {e}")
        return None

def process_large_csv_in_chunks(csv_path):
    """Lab 8: Loads CSV in chunks to compute global statistics and group by language."""
    if not csv_path or not os.path.exists(csv_path): return
    logging.info("--- Processing CSV in Chunks ---")
    
    chunk_size = 10  
    total_price = 0
    total_records = 0
    
    # Process chunks to calculate global mean
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        if 'price' in chunk.columns:
            cleaned_price = chunk['price'].replace('[\$,Free]', '', regex=True)
            cleaned_price = pd.to_numeric(cleaned_price, errors='coerce').fillna(0)
            total_price += cleaned_price.sum()
        total_records += len(chunk)
        
    global_mean = total_price / total_records if total_records > 0 else 0
    print(f"\n--- Chunk Processing Results ---")
    print(f"Total Records Processed: {total_records}")
    print(f"Global Mean Price Computed via Chunks: ${global_mean:.2f}")

def optimize_dataframe(df):
    """Lab 8: Optimizes dtypes to save memory and logs the reduction."""
    original_mem = df.memory_usage(deep=True).sum() / (1024 * 1024)
    
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer' if df[col].dtype == 'int64' else 'float')
        
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  
            df[col] = df[col].astype('category')
            
    optimized_mem = df.memory_usage(deep=True).sum() / (1024 * 1024)
    
    log_msg = f"Memory Optimization: {original_mem:.4f} MB -> {optimized_mem:.4f} MB"
    print(f"\n{log_msg}")
    logging.info(log_msg)
    
    return df