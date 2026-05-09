import pandas as pd
import pymysql
from sqlalchemy import create_engine
import logging
import os

def get_mysql_engine():
    """Creates a SQLAlchemy engine for MySQL connection."""
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "ahmad2004")
    host = os.getenv("MYSQL_HOST", "localhost")
    db = os.getenv("MYSQL_DB", "unstructured_data")
    
    try:
        # Creates a database if one doesn't exist using basic pymysql
        conn = pymysql.connect(host=host, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        conn.close()
        
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")
        return engine
    except Exception as e:
        logging.error(f"MySQL connection failed: {e}")
        return None

def populate_financials(df, table_name="course_financials"):
    """Saves cleaned financial data (prices, etc) to MySQL."""
    engine = get_mysql_engine()
    if engine and not df.empty:
        try:
            # Select relevant columns for the SQL table
            cols_to_save = [col for col in ['id', 'title', 'price', 'num_reviews', 'published_title'] if col in df.columns]
            df_sql = df[cols_to_save].copy()
            df_sql.to_sql(table_name, con=engine, if_exists='replace', index=False)
            logging.info(f"Successfully saved {len(df_sql)} records to MySQL table '{table_name}'.")
            return True
        except Exception as e:
            logging.error(f"Failed to populate MySQL: {e}")
    return False

def query_financials(table_name="course_financials"):
    """Reads data back from MySQL into a DataFrame."""
    engine = get_mysql_engine()
    if engine:
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, con=engine)
            logging.info(f"Queried {len(df)} records from MySQL.")
            return df
        except Exception as e:
            logging.error(f"Failed to query MySQL: {e}")
    return pd.DataFrame()