import pandas as pd
import logging

def convert_types(df):
    """Converts columns to their logical data types."""
    df = df.copy()
    
    # 1. Convert price to numeric (handling the '$' and 'Free' cases)
    if 'price' in df.columns:
        df['price'] = df['price'].replace('[\$,Free]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
        
    # 2. Convert date strings to datetime objects
    # Adjust 'published_title' or similar date columns if they exist in your data
    date_cols = [col for col in df.columns if 'date' in col.lower() or 'timestamp' in col.lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        
    # 3. Categorical conversion for low-cardinality strings
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() < 20: # Example threshold
            df[col] = df[col].astype('category')
            
    logging.info("Data types converted successfully.")
    return df