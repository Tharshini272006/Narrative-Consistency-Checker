import pathway as pw
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return model.encode(text).tolist()

def build_index(chunks):
    table = pw.debug.table_from_rows(
        [(c["id"], c["text"], c["time"], embed(c["text"])) for c in chunks],
        schema=["id", "text", "time", "embedding"]
    )

    index = pw.ml.index.KNNIndex(
        table,
        vector_column="embedding",
        metadata_columns=["text", "time"]
    )

    return index

def retrieve(index, query, k=5):
    query_vec = embed(query)
    results = index.search(query_vec, k=k)
    return results
