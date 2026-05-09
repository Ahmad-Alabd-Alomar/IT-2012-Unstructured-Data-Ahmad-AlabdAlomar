import pandas as pd
import logging

def perform_groupby_analysis(df):
    """Computes grouped summaries using multiple aggregation functions."""
    group_col = 'locale' if 'locale' in df.columns else (df.columns[1] if len(df.columns) > 1 else None)
    
    if not group_col or 'price' not in df.columns:
        logging.warning("Missing columns for groupby analysis.")
        return None
        
    grouped = df.groupby(group_col).agg(
        avg_price=('price', 'mean'),
        total_revenue=('price', 'sum'),
        course_count=('course_id', 'count'),
        median_price=('price', 'median')
    ).reset_index()
    
    logging.info(f"Grouped analysis completed for {group_col}.")
    return grouped
    
def get_top_n_per_group(df, group_col='locale', sort_col='price', n=3):
    """Finds the top N items per group using apply()."""
    if group_col not in df.columns or sort_col not in df.columns:
        return df
        
    # We remove 'drop=True' so that the 'locale' column is preserved after resetting the index
    top_n = df.groupby(group_col).apply(lambda x: x.nlargest(n, sort_col)).reset_index(level=0, drop=True).reset_index()
    
    # Alternatively, a cleaner modern way:
    # top_n = df.groupby(group_col, group_keys=False).apply(lambda x: x.nlargest(n, sort_col)).reset_index()
    
    return top_n