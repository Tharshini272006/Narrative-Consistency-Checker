def extract_claims(backstory_text):
    """
    Deterministic claim extraction for hackathon stability.
    Splits backstory into sentences and assigns heuristic claim types.
    """

    claims = []
    sentences = [s.strip() for s in backstory_text.split(".") if s.strip()]

    for s in sentences[:6]:
        s_lower = s.lower()

        if any(word in s_lower for word in ["trauma", "betray", "loss", "abuse"]):
            ctype = "TRAUMA"
        elif any(word in s_lower for word in ["believe", "belief", "trust", "distrust"]):
            ctype = "BELIEF"
        elif any(word in s_lower for word in ["world", "society", "authority", "institution"]):
            ctype = "WORLD_ASSUMPTION"
        elif any(word in s_lower for word in ["goal", "aim", "seek", "want", "ambition"]):
            ctype = "GOAL"
        else:
            ctype = "BELIEF"

        claims.append({
            "claim": s,
            "type": ctype
        })

    return claims
