import pandas as pd
import os
import logging
from src.cleaning.missing_handler import handle_missing_values, report_missing
from src.cleaning.string_cleaner import clean_strings
from src.cleaning.deduplicator import remove_duplicates
from src.cleaning.type_converter import convert_types
from src.cleaning.validator import validate_data
from src.analytics.regex_ops import validate_and_clean_regex

def run_cleaning_pipeline(input_csv="data/raw/analytics_export.csv", 
                          output_csv="data/processed/cleaned/cleaned_data.csv"):
    """Executes the full cleaning workflow."""
    logging.info("--- Starting Data Cleaning Pipeline ---")
    
    if not os.path.exists(input_csv):
        logging.error(f"Input file {input_csv} not found. Run Lab 8 first.")
        return None
        
    # Load
    df = pd.read_csv(input_csv)
    
    # Execute steps
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = clean_strings(df)
    df = convert_types(df)
    df = validate_and_clean_regex(df) # From Lab 8/9 update
    
    # Validate
    validate_data(df)
    
    # Save
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    logging.info(f"Cleaned data saved to {output_csv}")
    print(f"Done! Cleaned data saved to {output_csv}")
    return output_csv