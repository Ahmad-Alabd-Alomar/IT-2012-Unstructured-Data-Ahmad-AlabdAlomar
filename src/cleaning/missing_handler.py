import pandas as pd
import logging

def report_missing(df):
    """Generates a missing-value report."""
    missing = df.isnull().sum()
    print("--- Missing Values Report ---")
    print(missing[missing > 0])
    return missing

def handle_missing_values(df):
    """Applies different strategies to resolve missing data."""
    df = df.copy()
    
    # Drop rows missing critical identifiers (assuming 'id' or 'title' exists)
    critical_cols = [col for col in ['id', 'title'] if col in df.columns]
    if critical_cols:
        df = df.dropna(subset=critical_cols)
        
    # Replace unrealistic zero values with NaN (e.g., price = 0)
    if 'price' in df.columns:
        df['price'] = df['price'].replace(0, pd.NA)
        
    # Fill numeric missing values with medians
    for col in df.select_dtypes(include=['number']).columns:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        
    # Fill descriptive text fields with placeholders
    for col in df.select_dtypes(include=['object', 'category']).columns:
        df[col] = df[col].fillna("Unknown")
        
    # Drop columns whose missing-data ratio is too high (> 50%)
    threshold = 0.5 * len(df)
    df = df.dropna(thresh=threshold, axis=1)
    
    logging.info("Handled missing values.")
    return df