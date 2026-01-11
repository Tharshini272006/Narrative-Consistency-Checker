from pipeline.chunk import chunk_text
from pipeline.index import build_index
from pipeline.claims import extract_claims
from pipeline.consistency import check_temporal_consistency
from pipeline.decision import final_decision
import csv

print("\n" + "=" * 60)
print("KDSH — BACKSTORY CONSISTENCY CHECK")
print("=" * 60)

# -------------------------------------------------
# LOAD INPUTS (DYNAMIC — JUDGE CAN CHANGE THESE)
# -------------------------------------------------
with open("data/novel.txt", "r", encoding="utf-8") as f:
    novel_text = f.read()

with open("data/backstory.txt", "r", encoding="utf-8") as f:
    backstory_text = f.read()

print("Novel length (characters):", len(novel_text))
print("Backstory length (characters):", len(backstory_text))

# -------------------------------------------------
# STEP 1: CHUNKING
# -------------------------------------------------
print("\nChunking novel...")
chunks = chunk_text(novel_text)
print("Total chunks created:", len(chunks))

# -------------------------------------------------
# STEP 2: INDEXING (Pathway / Embeddings)
# -------------------------------------------------
print("\nBuilding retrieval index...")
index = build_index(chunks)

# -------------------------------------------------
# STEP 3: CLAIM EXTRACTION
# -------------------------------------------------
print("\nEXTRACTING CLAIMS FROM BACKSTORY...")
claims = extract_claims(backstory_text)

print("\nCLAIMS FOUND:")
for c in claims:
    print("-", c)

# -------------------------------------------------
# STEP 4: TEMPORAL CONSISTENCY CHECK
# -------------------------------------------------
print("\nCHECKING TEMPORAL CONSISTENCY...")
temporal_map = check_temporal_consistency(
    claims=claims,
    index=index
)

print("\nDEBUG: Temporal Map Used for Decision")
print("=" * 60)
for c in temporal_map:
    print(c)

# -------------------------------------------------
# STEP 5: FINAL DECISION
# -------------------------------------------------
print("\nFINAL CONSISTENCY DECISION")
print("=" * 60)

prediction = final_decision(temporal_map)
label = "CONSISTENT" if prediction == 1 else "CONTRADICTION"

print("Prediction:", prediction, "-", label)

# -------------------------------------------------
# STEP 6: SAVE RESULTS
# -------------------------------------------------
with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["story_id", "prediction"])
    writer.writerow([1, prediction])

print("\nresults.csv generated successfully")
print("=" * 60)
