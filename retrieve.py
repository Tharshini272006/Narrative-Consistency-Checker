from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, chunks, top_k=5):
    query_emb = model.encode([query])[0]

    scored = []
    for c in chunks:
        emb = model.encode([c["text"]])[0]
        score = np.dot(query_emb, emb)
        scored.append((score, c))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [c for _, c in scored[:top_k]]
