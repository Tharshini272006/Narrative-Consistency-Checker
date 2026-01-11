from sentence_transformers import SentenceTransformer
import numpy as np

def build_index(chunks):
    """
    chunks: list of dicts
    [
      {
        "text": "...",
        "time": "early" | "mid" | "late"
      }
    ]
    """

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)

    index = []
    for i, c in enumerate(chunks):
        index.append({
            "embedding": embeddings[i],
            "text": c["text"],
            "time": c["time"]
        })

    return index
