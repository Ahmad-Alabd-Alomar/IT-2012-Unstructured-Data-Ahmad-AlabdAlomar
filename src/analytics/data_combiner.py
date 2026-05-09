import pandas as pd
import logging

def combine_dataframes(df1, df2, join_key='id'):
    """Merges two DataFrames on a common key and compares join types."""
    if df1.empty or df2.empty or join_key not in df1.columns or join_key not in df2.columns:
        logging.warning("Cannot combine DataFrames: Empty data or missing join key.")
        return None

    print(f"--- Join Comparisons on '{join_key}' ---")
    
    # Inner Join
    inner_df = pd.merge(df1, df2, on=join_key, how='inner')
    print(f"Inner Join rows: {len(inner_df)}")
    
    # Left Join
    left_df = pd.merge(df1, df2, on=join_key, how='left')
    print(f"Left Join rows:  {len(left_df)}")
    
    # Right Join
    right_df = pd.merge(df1, df2, on=join_key, how='right')
    print(f"Right Join rows: {len(right_df)}")
    
    # Outer Join
    outer_df = pd.merge(df1, df2, on=join_key, how='outer')
    print(f"Outer Join rows: {len(outer_df)}")

    logging.info("DataFrames combined successfully.")
    
    return inner_df