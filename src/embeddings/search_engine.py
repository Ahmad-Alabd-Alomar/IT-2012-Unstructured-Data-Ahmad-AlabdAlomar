import pandas as pd
import sys
import os
import logging

# Path Fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.embeddings.chroma_store import ChromaStoreManager
from src.embeddings.hybrid_search import reciprocal_rank_fusion

class SearchEngine:
    def __init__(self, df_path="data/processed/cleaned/cleaned_data.csv"):
        if not os.path.exists(df_path):
            raise FileNotFoundError(f"Cleaned data not found at {df_path}")
            
        self.df = pd.read_csv(df_path)
        self.store = ChromaStoreManager()
        
        # Ensure database is synced with current CSV
        self._sync_database()

    def _sync_database(self):
        """Forces the CSV data into ChromaDB with correct types."""
        docs = [f"Course: {row['title']}. Instructor: {row['instructor']}." for _, row in self.df.iterrows()]
        ids = [str(row['course_id']) for _, row in self.df.iterrows()]
        metas = [
            {
                "title": str(r['title']), 
                "instructor": str(r['instructor']).lower(), 
                "price": float(r['price'])
            } for _, r in self.df.iterrows()
        ]
        self.store.add_data(ids, docs, metas)

    def keyword_search(self, query, n_results=5):
        """Standard word-match search."""
        query = query.lower()
        mask = self.df['title'].str.lower().str.contains(query) | self.df['instructor'].str.lower().str.contains(query)
        results = self.df[mask].head(n_results)
        return results['course_id'].astype(str).tolist(), results['title'].tolist()

    def semantic_search(self, query, n_results=5):
        """Meaning-based search using vectors."""
        res = self.store.semantic_query(query, n_results=n_results)
        return res['ids'][0], [m['title'] for m in res['metadatas'][0]]

    def hybrid_search(self, query, n_results=5):
        """Combines results using Reciprocal Rank Fusion (RRF)."""
        k_ids, _ = self.keyword_search(query, n_results=10)
        s_ids, _ = self.semantic_search(query, n_results=10)
        
        fused_scores = reciprocal_rank_fusion(k_ids, s_ids)
        top_ids = [item[0] for item in fused_scores[:n_results]]
        
        # Map IDs to Titles
        return self.df[self.df['course_id'].astype(str).isin(top_ids)]['title'].tolist()

if __name__ == "__main__":
    # Test it works
    engine = SearchEngine()
    print("SearchEngine initialized and synced!")
