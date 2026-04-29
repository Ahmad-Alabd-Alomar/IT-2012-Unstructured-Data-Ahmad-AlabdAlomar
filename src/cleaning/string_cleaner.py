import pandas as pd
import logging

def clean_strings(df):
    """Cleans text columns by fixing whitespace, casing, and formats."""
    df = df.copy()
    
    text_cols = df.select_dtypes(include=['object']).columns
    
    for col in text_cols:
        # Convert to string to avoid errors on mixed types
        df[col] = df[col].astype(str)
        # Normalise case (title case for names/titles, lower for others if needed)
        if col == 'title':
            df[col] = df[col].str.title()
        else:
             df[col] = df[col].str.lower()
        # Remove extra whitespace
        df[col] = df[col].str.strip().replace(r'\s+', ' ', regex=True)
        
    logging.info("String columns cleaned.")
    return df