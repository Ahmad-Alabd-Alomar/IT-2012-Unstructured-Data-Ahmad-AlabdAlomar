import pytest
import pandas as pd
import numpy as np
from src.cleaning.string_cleaner import clean_strings
from src.cleaning.deduplicator import remove_duplicates
from src.cleaning.missing_handler import handle_missing_values

def test_string_cleaning():
    """Test that strings are trimmed and title-cased."""
    test_df = pd.DataFrame({'title': ['  python course  ', 'JAVA basics']})
    cleaned = clean_strings(test_df)
    assert cleaned.iloc[0]['title'] == 'Python Course'
    assert cleaned.iloc[1]['title'] == 'Java Basics'

def test_deduplication():
    """Test that duplicates are removed."""
    test_df = pd.DataFrame({'id': [1, 1, 2], 'val': ['a', 'a', 'b']})
    cleaned = remove_duplicates(test_df)
    assert len(cleaned) == 2

def test_missing_handler():
    """Test that missing values in numeric columns are filled with median."""
    test_df = pd.DataFrame({'price': [10, 20, np.nan]})
    cleaned = handle_missing_values(test_df)
    assert cleaned['price'].isnull().sum() == 0
    assert cleaned.iloc[2]['price'] == 15.0 # Median of 10 and 20