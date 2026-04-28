import pandas as pd
import logging

def clean_text_with_regex(df):
    """Lab 8: 4+ Regex operations on title, overview, or content columns."""
    logging.info("--- Running Regex Text Cleaning ---")
    
    # Target 'title' column primarily
    col = 'title' if 'title' in df.columns else df.columns[0]
    
    # Operation 1: Remove special characters/emojis from titles
    df[f'{col}_clean'] = df[col].str.replace(r'[^\w\s]', '', regex=True)
    
    # Operation 2: Convert to lowercase
    df[f'{col}_clean'] = df[f'{col}_clean'].str.lower()
    
    # Operation 3: Remove extra whitespace
    df[f'{col}_clean'] = df[f'{col}_clean'].str.strip().replace(r'\s+', ' ', regex=True)
    
    # Operation 4: Identify rows containing "Python" (Case insensitive)
    python_mentions = df[col].str.contains(r'python', case=False, na=False).sum()
    
    print(f"\n--- Regex Cleaning ---")
    print(f"Sample Cleaned Titles: \n{df[f'{col}_clean'].head(3)}")
    print(f"Total rows mentioning 'Python': {python_mentions}")
    
    return df