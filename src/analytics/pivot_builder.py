import pandas as pd
import logging
import os

def reshape_to_long(df):
    """Converts wide data to long format using melt()."""
    cols_to_melt = [c for c in ['price', 'num_reviews', 'num_subscribers'] if c in df.columns]
    id_vars = [c for c in ['id', 'title'] if c in df.columns]
    
    if not cols_to_melt or not id_vars:
        return df
        
    long_df = df.melt(id_vars=id_vars, value_vars=cols_to_melt, 
                      var_name='metric', value_name='value')
    logging.info(f"Reshaped to long format. New shape: {long_df.shape}")
    return long_df

def build_pivot_table(df, save_dir="data/processed/analytics"):
    """Creates a multi-dimensional summary pivot table."""
    index_col = 'published_title' if 'published_title' in df.columns else (df.columns[0] if len(df.columns) > 0 else None)
    col_group = 'locale' if 'locale' in df.columns else (df.columns[1] if len(df.columns) > 1 else None)
    value_col = 'price' if 'price' in df.columns else None

    if not index_col or not col_group or not value_col:
        logging.warning("Missing columns for pivot table.")
        return None
        
    if 'date' in index_col.lower() or 'published' in index_col.lower():
        df['year'] = pd.to_datetime(df[index_col], errors='coerce').dt.year
        index_col = 'year'

    pivot_df = pd.pivot_table(df, values=value_col, index=index_col, 
                              columns=col_group, aggfunc='mean', margins=True)
    
    # Save the result
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "pivot_price_by_year_and_locale.csv")
    pivot_df.to_csv(save_path)
    logging.info(f"Pivot table saved to {save_path}")
    
    return pivot_df