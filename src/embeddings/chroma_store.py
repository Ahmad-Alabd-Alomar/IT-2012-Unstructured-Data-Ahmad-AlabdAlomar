import chromadb
import os
from chromadb.utils import embedding_functions
class ChromaStoreManager:
    def __init__(self, db_path="data/embeddings/chroma_db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="data", embedding_function=self.emb_fn)
    def add_data(self, ids, documents, metadatas):
        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    def semantic_query(self, query_text, n_results=5, filter_dict=None):
        return self.collection.query(query_texts=[query_text], n_results=n_results, where=filter_dict)
