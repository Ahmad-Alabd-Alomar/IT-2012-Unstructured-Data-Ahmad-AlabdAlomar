import logging
import os
from src.analytics.db_connector import query_financials
from src.analytics.mongo_pipeline import run_mongo_aggregation

def generate_report():
    """Runs key analytics and generates a high-level automated summary."""
    logging.info("Starting automated insight generation...")
    os.makedirs("data/processed/analytics", exist_ok=True)
    
    # 1. Fetch data
    df_sql = query_financials()
    df_mongo = run_mongo_aggregation()
    
    # 2. Write report
    report_path = "data/processed/analytics/automated_insights.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=== Automated Pipeline Analytics Report ===\n")
        f.write(f"Valid Financial Records in MySQL: {len(df_sql) if df_sql is not None else 0}\n")
        
        if df_mongo is not None and not df_mongo.empty:
            top_locale = df_mongo.iloc[0]['locale']
            top_count = df_mongo.iloc[0]['course_count']
            f.write(f"Top Performing Language (MongoDB): {top_locale} with {top_count} courses.\n")
            
    logging.info(f"Insight report successfully saved to {report_path}")
    return True