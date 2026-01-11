from sentence_transformers import SentenceTransformer, util

def check_temporal_consistency(claims, indexed_chunks, threshold=0.55):
    """
    claims: list of dicts
      [{"claim": "...", "type": "..."}]

    indexed_chunks: output of build_index()
    """

    model = SentenceTransformer("all-MiniLM-L6-v2")

    temporal_map = []

    for claim_obj in claims:
        claim_text = claim_obj["claim"]
        claim_emb = model.encode(claim_text, convert_to_tensor=True)

        result = {
            "claim": claim_text,
            "type": claim_obj["type"],
            "early": "SUPPORTED_OR_NEUTRAL",
            "mid": "SUPPORTED_OR_NEUTRAL",
            "late": "SUPPORTED_OR_NEUTRAL",
        }

        for chunk in indexed_chunks:
            score = util.cos_sim(claim_emb, chunk["embedding"]).item()

            if score > threshold:
                if any(x in claim_text.lower() for x in ["distrust", "avoid", "skeptic"]):
                    result[chunk["time"]] = "CONTRADICTED"

        temporal_map.append(result)

    return temporal_map
