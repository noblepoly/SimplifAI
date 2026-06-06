import streamlit as st
from backend import extract_source_concepts

# 1. Workflow Initialization: Set up the memory bank
if "workflow_stage" not in st.session_state:
    st.session_state["workflow_stage"] = "ingestion"
if "cached_concepts" not in st.session_state:
    st.session_state["cached_concepts"] = None

# --- Topographical Layout ---
st.title("CogniStruct: Active Recall Engine")
st.markdown("Master complex subjects through the Feynman Technique.")
st.divider()

# 2. Phase One: Source Text Ingestion
if st.session_state["workflow_stage"] == "ingestion":
    st.subheader("Step 1: Ingest Source Material")
    
    source_text = st.text_area(
        "Paste your academic text here:", 
        height=200, 
        placeholder="Photosynthesis is the process used by plants..."
    )
    
    if st.button("Extract Concepts"):
        if source_text.strip():
            with st.spinner("Analyzing text and extracting core concepts..."):
                # Call our verified deterministic backend
                extracted_data = extract_source_concepts(source_text)
                
                # Cache the results securely in memory
                st.session_state["cached_concepts"] = extracted_data.extracted_concepts
                
                # Mutate the state to transition the UI to Phase Two
                st.session_state["workflow_stage"] = "active_recall"
                st.rerun()
        else:
            st.error("Please paste some text before extracting.")

# 3. Phase Two: The Active Recall Form
elif st.session_state["workflow_stage"] == "active_recall":
    st.subheader("Step 2: The Feynman Technique")
    st.info("Explain these concepts in your own words. Do not look at the source text!")
    
    # We use a form to suspend Streamlit's rerun behavior until the user is completely done typing
    with st.form("feynman_form"):
        user_explanations = {}
        
        # Iterate over the safe, type-checked Pydantic objects we cached in memory
        for idx, concept in enumerate(st.session_state["cached_concepts"]):
            st.markdown(f"**Concept {idx + 1}: {concept.concept_title}**")
            # Create a text area for each concept
            user_explanations[concept.concept_title] = st.text_area(
                f"Explain '{concept.concept_title}':", 
                key=f"input_{idx}"
            )
            st.markdown("---")
            
        # The form submit button
        submitted = st.form_submit_button("Submit Explanations for Evaluation")
        
        if submitted:
            # Here is where the final evaluation logic will go!
            st.success("Explanations submitted! (Evaluation backend coming next)")
            
    # Allow the user to reset the app
    if st.button("Start Over"):
        st.session_state["workflow_stage"] = "ingestion"
        st.session_state["cached_concepts"] = None
        st.rerun()