import os
import pandas as pd
import matplotlib.pyplot as plt
import logging

def run_eda(csv_path):
    """Lab 8: Exploratory Data Analysis & Visualization."""
    if not csv_path or not os.path.exists(csv_path): return
    logging.info("--- Starting Exploratory Data Analysis ---")
    
    df = pd.read_csv(csv_path)
    
    print("\n--- EDA: Dataset Overview ---")
    print(f"Shape: {df.shape}")
    print("\nInfo:")
    df.info()
    print("\nDescribe (Numeric Stats):")
    print(df.describe())
    

    categorical_col = 'type' if 'type' in df.columns else df.columns[0]
    
    print(f"\nValue Counts for '{categorical_col}':")
    print(df[categorical_col].value_counts().head(5))
    print(f"Unique values in '{categorical_col}': {df[categorical_col].nunique()}")
    
    output_dir = "data/processed/analytics"
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    df[categorical_col].value_counts().head(10).plot(kind='bar', color='steelblue')
    plt.title(f"Distribution of {categorical_col}")
    plt.xlabel(categorical_col)
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart_path = os.path.join(output_dir, f"{categorical_col}_distribution.png")
    plt.savefig(chart_path)
    logging.info(f"Saved EDA chart to {chart_path}")
    plt.close()