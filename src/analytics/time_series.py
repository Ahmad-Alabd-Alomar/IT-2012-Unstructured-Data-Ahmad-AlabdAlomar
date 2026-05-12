import pandas as pd
import logging

def analyze_time_series(df, date_col='published_title', val_col='price'):
    """Parses dates, extracts components, and calculates rolling averages."""
    if date_col not in df.columns or val_col not in df.columns:
        logging.warning("Missing date or value column for time series.")
        return None
        
    df = df.copy()
    
    # 1. Parse to datetime64
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    
    # 2. Extract 3 date components
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['day_of_week'] = df[date_col].dt.day_name()
    
    # 3. Build monthly time series & resample to yearly
    df.set_index(date_col, inplace=True)
    monthly_ts = df[val_col].resample('ME').mean().fillna(0)
    yearly_ts = monthly_ts.resample('YE').mean()
    
    # 4. Compute rolling averages (windows: 3, 6, 12)
    rolling_df = pd.DataFrame({
        'monthly_avg': monthly_ts,
        'rolling_3': monthly_ts.rolling(window=3).mean(),
        'rolling_6': monthly_ts.rolling(window=6).mean(),
        'rolling_12': monthly_ts.rolling(window=12).mean()
    })
    
    logging.info("Time series analysis complete.")
    return rolling_df