import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging

def generate_quality_report(df, output_dir="data/processed/analytics"):
    """Lab 8: Missing value analysis, heatmap, and full quality audit."""
    logging.info("--- Generating Data Quality Report ---")
    os.makedirs(output_dir, exist_ok=True)

    # 1. Missing Value Analysis
    missing_count = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100
    
    # 2. Duplicate Detection
    duplicates = df.duplicated().sum()

    # 3. Visualization: Missing Data Heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
    plt.title("Missing Data Heatmap")
    heatmap_path = os.path.join(output_dir, "missing_data_heatmap.png")
    plt.savefig(heatmap_path)
    plt.close()
    
    # 4. Construct Quality Report DataFrame
    quality_df = pd.DataFrame({
        'Column': df.columns,
        'Missing Values': missing_count,
        'Missing Percentage (%)': missing_pct,
        'Unique Values': [df[col].nunique() for col in df.columns],
        'Dtype': df.dtypes
    })
    
    report_path = os.path.join(output_dir, "data_quality_report.csv")
    quality_df.to_csv(report_path, index=False)
    
    print(f"\n--- Data Quality Summary ---")
    print(f"Total Duplicates Found: {duplicates}")
    print(f"Quality report saved to: {report_path}")
    print(f"Heatmap saved to: {heatmap_path}")
    
    logging.info(f"Quality report and heatmap generated in {output_dir}")