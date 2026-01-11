import streamlit as st
import pandas as pd

from pipeline.chunk import chunk_text
from pipeline.index import build_index
from pipeline.claims import extract_claims
from pipeline.consistency import check_temporal_consistency
from pipeline.decision import final_decision


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Narrative Consistency Checker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SIDEBAR (INSTRUCTIONS)
# =========================================================
st.sidebar.title("How to Use")

st.sidebar.markdown(
    """
    **Goal**  
    Check whether a hypothetical character backstory is
    logically consistent with a full novel.

    **Steps**
    1. Upload the novel text (`.txt`)
    2. Upload a character backstory (`.txt`)
    3. Click **Run Consistency Check**

    **Output**
    - Extracted claims from backstory  
    - Temporal evidence (early / mid / late)
    - Final consistency decision
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Decision Labels**
    - ✅ **Consistent (1)**  
      Backstory can plausibly lead to the novel’s events
    - ❌ **Contradiction (0)**  
      Backstory conflicts with narrative evidence
    """
)

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div style='background-color:#2E4053;padding:22px;border-radius:6px'>
        <h1 style='color:white;text-align:center'>
            Narrative Consistency Checker
        </h1>
        <p style='color:white;text-align:center;font-size:16px'>
            Evaluating long-term character consistency in long-form narratives
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# =========================================================
# INPUT SECTION
# =========================================================
st.subheader("Upload Inputs")

col1, col2 = st.columns(2)

with col1:
    novel_file = st.file_uploader(
        "Upload Novel (.txt)",
        type=["txt"]
    )

with col2:
    backstory_file = st.file_uploader(
        "Upload Backstory (.txt)",
        type=["txt"]
    )

st.write("")
run_check = st.button("Run Consistency Check")

# =========================================================
# MAIN PIPELINE
# =========================================================
if run_check:

    if not novel_file or not backstory_file:
        st.error("Please upload both the novel and the backstory.")
        st.stop()

    with st.spinner("Running consistency analysis..."):

        novel_text = novel_file.read().decode("utf-8")
        backstory_text = backstory_file.read().decode("utf-8")

        chunks = chunk_text(novel_text)
        indexed_chunks = build_index(chunks)

        claims = extract_claims(backstory_text)
        temporal_map = check_temporal_consistency(claims, indexed_chunks)

        prediction = final_decision(temporal_map)

    # =====================================================
    # OUTPUT: CLAIMS
    # =====================================================
    st.markdown("---")
    st.subheader("🔍 Extracted Backstory Claims")

    for i, c in enumerate(claims, 1):
        st.markdown(f"**{i}. ({c['type']})** {c['claim']}")

    # =====================================================
    # OUTPUT: TEMPORAL MAP
    # =====================================================
    st.write("")
    st.subheader("📊 Temporal Consistency Analysis")

    table_rows = []
    for c in temporal_map:
        table_rows.append({
            "Claim": c["claim"],
            "Type": c["type"],
            "Early": c["early"],
            "Mid": c["mid"],
            "Late": c["late"]
        })

    df = pd.DataFrame(table_rows)
    st.dataframe(df, use_container_width=True)

    # =====================================================
    # FINAL DECISION
    # =====================================================
    st.write("")
    st.subheader("🏁 Final Decision")

    if prediction == 1:
        st.success("✔ The backstory is CONSISTENT with the novel.")
    else:
        st.error("✘ The backstory CONTRADICTS the novel.")

    # =====================================================
    # DOWNLOAD RESULTS
    # =====================================================
    result_df = pd.DataFrame(
        [{"story_id": 1, "prediction": prediction}]
    )

    csv_data = result_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download results.csv",
        data=csv_data,
        file_name="results.csv",
        mime="text/csv"
    )

    st.caption("Analysis completed successfully.")
