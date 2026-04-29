import pandas as pd
import logging

def remove_duplicates(df):
    """Removes exact duplicates and duplicates based on unique IDs."""
    df = df.copy()
    initial_count = len(df)
    
    # 1. Remove exact duplicate rows
    df = df.drop_duplicates()
    
    # 2. Remove duplicates based on a specific column if it exists (like 'id' from Udemy)
    if 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'])
    
    final_count = len(df)
    removed = initial_count - final_count
    
    log_msg = f"Deduplication: Started with {initial_count}, finished with {final_count}. Removed {removed} rows."
    print(log_msg)
    logging.info(log_msg)
    
    return df