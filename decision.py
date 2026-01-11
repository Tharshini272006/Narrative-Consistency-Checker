def final_decision(temporal_map):
    """
    temporal_map format:
    {
      claim: {
        "type": "...",
        "early": "CONTRADICTED / SUPPORTED_OR_NEUTRAL",
        "mid": "...",
        "late": "..."
      }
    }
    """

    belief_contradictions = 0

    for claim, data in temporal_map.items():
        ctype = data["type"]

        early = data["early"]
        mid = data["mid"]

        if ctype == "WORLD_ASSUMPTION":
            if "CONTRADICTED" in [early, mid]:
                return 0

        if ctype == "TRAUMA":
            if "CONTRADICTED" in [early, mid]:
                return 0

        if ctype == "BELIEF":
            if "CONTRADICTED" in [early, mid]:
                belief_contradictions += 1

    if belief_contradictions >= 2:
        return 0

    return 1
