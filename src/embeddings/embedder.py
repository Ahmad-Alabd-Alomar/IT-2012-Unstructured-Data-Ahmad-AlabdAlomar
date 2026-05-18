import torch
from sentence_transformers import SentenceTransformer, util
_model = SentenceTransformer("all-MiniLM-L6-v2")
def generate_embeddings(texts):
    return _model.encode(texts, normalize_embeddings=True)
def calculate_all_metrics(emb_a, emb_b):
    a, b = torch.tensor(emb_a), torch.tensor(emb_b)
    return {
        "cosine": round(util.cos_sim(a, b).item(), 4),
        "dot_product": round(torch.dot(a, b).item(), 4),
        "euclidean": round(torch.dist(a, b).item(), 4)
    }
def prepare_course_text(row):
    return f"Course: {row['title']}. Instructor: {row['instructor']}."
