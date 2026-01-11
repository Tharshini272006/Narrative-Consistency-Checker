def chunk_text(text, chunk_size=4000, overlap=800):
    chunks = []
    start = 0
    chunk_id = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end]

        position_ratio = chunk_id / max(1, (length // chunk_size))
        if position_ratio < 0.33:
            time = "early"
        elif position_ratio < 0.66:
            time = "mid"
        else:
            time = "late"

        chunks.append({
            "id": chunk_id,
            "text": chunk,
            "time": time
        })

        start = end - overlap
        chunk_id += 1

    return chunks
