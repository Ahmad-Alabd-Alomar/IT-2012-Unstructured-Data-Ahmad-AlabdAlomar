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
    
    # FIX: Return the dataframe so the pipeline can continue!
    return df

def validate_and_clean_regex(df):
    """Detects, validates, and cleans complex text patterns."""
    df = df.copy()
    
    if 'language' in df.columns:
        # Detect invalid language codes
        invalid_langs = df[~df['language'].str.match(r'^[a-z]{2}$', na=False)]
        print(f"Found {len(invalid_langs)} invalid language codes.")
        
    if 'overview' in df.columns:
        # Flag overviews that are too short (< 20 characters)
        df['short_overview'] = df['overview'].str.len() < 20
        
    logging.info("Regex validation and cleaning completed.")
    
    return df
