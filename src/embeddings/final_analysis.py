import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.embeddings.search_engine import SearchEngine

def run_lab11_questions():
    engine = SearchEngine()
    print("\n" + "="*60)
    print("       LAB 11 - PART 7: ANALYTICAL DATA QUESTIONS")
    print("="*60)

    # Question 1: Price and Keyword constraint
    print("\n[Q1] Find 'Basic' Python courses that cost less than $45.")
    q1_filter = {"price": {"$lt": 45.0}}
    res1 = engine.store.semantic_query("basic introduction", n_results=2, filter_dict=q1_filter)
    for i in range(len(res1['ids'][0])):
        m = res1['metadatas'][0][i]
        print(f" >> Found: {m['title']} | Price: ${m['price']}")

    # Question 2: Instructor Exclusion and Meaning search
    print("\n[Q2] Find 'Advanced' topics NOT taught by 'Michael Kennedy'.")
    q2_filter = {"instructor": {"$ne": "michael kennedy"}}
    res2 = engine.store.semantic_query("advanced expert complex", n_results=2, filter_dict=q2_filter)
    for i in range(len(res2['ids'][0])):
        m = res2['metadatas'][0][i]
        print(f" >> Found: {m['title']} | Instructor: {m['instructor']}")

    # Question 3: Hybrid Search Comparison
    print("\n[Q3] Top recommendation for 'Python Data' using Hybrid RRF Search:")
    hybrid_results = engine.hybrid_search("Python Data", n_results=1)
    print(f" >> Top Hybrid Pick: {hybrid_results}")

    print("\n" + "="*60)
    print("             LAB 11 ANALYSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_lab11_questions()
