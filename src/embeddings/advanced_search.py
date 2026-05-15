import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.embeddings.chroma_store import ChromaStoreManager

def run_advanced_demo():
    store = ChromaStoreManager()
    
    print("\n" + "="*50)
    print("LAB 11 - PART 6: ADVANCED METADATA FILTERING")
    print("="*50)

    # SCENARIO 1: AND filter ($and)
    # Price < 60 AND instructor is NOT 'real python'
    print("\n--- Query 1: Affordable courses NOT from 'real python' ---")
    query1 = "Python programming"
    filter1 = {
        "$and": [
            {"price": {"$lt": 60.0}},
            {"instructor": {"$ne": "real python"}}
        ]
    }
    
    res1 = store.semantic_query(query1, n_results=3, filter_dict=filter1)
    
    if res1['ids'] and len(res1['ids'][0]) > 0:
        for i in range(len(res1['ids'][0])):
            m = res1['metadatas'][0][i]
            print(f" > {m['title']} | Instructor: {m['instructor']} | ${m['price']}")
    else:
        print("No results found for Query 1.")

    # SCENARIO 2: OR filter ($or)
    # Price < 40 OR instructor is 'michael kennedy'
    print("\n--- Query 2: Cheap courses OR Michael Kennedy's work ---")
    query2 = "Python updates"
    filter2 = {
        "$or": [
            {"price": {"$lt": 40.0}},
            {"instructor": {"$eq": "michael kennedy"}}
        ]
    }
    
    res2 = store.semantic_query(query2, n_results=3, filter_dict=filter2)
    
    if res2['ids'] and len(res2['ids'][0]) > 0:
        for i in range(len(res2['ids'][0])):
            m = res2['metadatas'][0][i]
            print(f" > {m['title']} | Instructor: {m['instructor']} | ${m['price']}")
    else:
        print("No results found for Query 2.")

    print("\n" + "="*50)
    print("LAB 11 COMPLETE")
    print("="*50)

if __name__ == "__main__":
    run_advanced_demo()
