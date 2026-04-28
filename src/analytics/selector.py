import pandas as pd
import logging

def demonstrate_selection(df):
    """Lab 8: Demonstrates loc, iloc, boolean indexing, isin, and between."""
    logging.info("--- Demonstrating pandas Selection Methods ---")
    
    if df.empty: return

    # 1. loc & iloc
    # Get first 5 rows and specific columns by name
    subset_loc = df.loc[:5, ['title', 'price']] if 'price' in df.columns else df.loc[:5, :2]
    # Get first 2 rows and first 3 columns by index position
    subset_iloc = df.iloc[:2, :3]

    # 2. Boolean Indexing
    if 'num_reviews' in df.columns:
        high_review_courses = df[df['num_reviews'] > 100]
    else:
        high_review_courses = df.head(2)

    # 3. isin
    if 'language' in df.columns:
        lang_filter = df[df['language'].isin(['en_US', 'es_ES'])]
    else:
        lang_filter = df.head(1)

    # 4. between
    if 'price' in df.columns:
        # Convert price to numeric for the filter
        numeric_price = pd.to_numeric(df['price'].replace('[\$,Free]', '', regex=True), errors='coerce')
        price_range = df[numeric_price.between(20, 50)]
    
    print("\n--- Selection Demonstration Completed ---")
    logging.info("Selection demonstration successful.")