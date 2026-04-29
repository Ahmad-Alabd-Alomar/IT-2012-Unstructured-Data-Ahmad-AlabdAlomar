import logging

def validate_data(df):
    """Performs logical checks and assertions on the cleaned dataset."""
    try:
        # 1. Check for duplicates
        assert df.duplicated().sum() == 0, "Validation Failed: Duplicates still exist!"
        
        # 2. Check for missing values in critical columns
        if 'title' in df.columns:
            assert df['title'].isnull().sum() == 0, "Validation Failed: Missing titles found!"
            
        # 3. Check numeric ranges (prices shouldn't be negative)
        if 'price' in df.columns:
            assert (df['price'] >= 0).all(), "Validation Failed: Negative prices detected!"
            
        print("✅ Data Validation Passed!")
        logging.info("Cleaned data validated successfully.")
        return True
    except AssertionError as e:
        print(f"❌ Data Validation Error: {e}")
        logging.error(f"Validation Error: {e}")
        return False