import numpy as np
import logging

def run_numpy_operations():
    """Lab 8: Array creation, inspection, and vectorized math without loops."""
    logging.info("--- Starting NumPy Operations ---")
    

    list_array = np.array([10, 20, 30, 40, 50])
    zeros_array = np.zeros((3, 3))
    range_array = np.arange(0, 100, 10)
    random_array = np.random.rand(5)


    print("\n--- NumPy Array Inspections ---")
    arrays = {"List Array": list_array, "Zeros Array": zeros_array, "Range Array": range_array, "Random Array": random_array}
    for name, arr in arrays.items():
        print(f"{name} -> Shape: {arr.shape}, Dtype: {arr.dtype}, Dimensions: {arr.ndim}")


    base_prices = np.array([19.99, 29.99, 49.99, 99.99])
    adjusted_prices = base_prices * 1.15  
    
    print("\n--- Vectorized Arithmetic ---")
    print(f"Base Prices: {base_prices}")
    print(f"Adjusted Prices (+15%): {adjusted_prices}")
    logging.info("NumPy operations completed successfully.")