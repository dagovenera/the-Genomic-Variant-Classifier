import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Genomic Variant Classifier", page_icon="🧬", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load("RandomForest_model.pkl")

artifacts = load_model()
model = artifacts["model"]
features = artifacts["features"]
target_map = artifacts["target_map"]

st.title("🧬 Genomic Mutations & Variants Classifier")
st.markdown(
    """
    **Bioinformatics Data Science Portfolio** | *Engineering Toolkit: Perl, SQL, Python, and Random Forest Multi-Class Modeling*  
    This interface parses input genetic variant features, transform them to one-hot-encoded arrays, and process them with 
    random forest models to forecast their clinical significance.
    """
)
st.write("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Input Genetic Variant Features")
    
    # Render selectors matching model features
    gene = st.selectbox("Select Gene", ["BRCA1", "EGFR", "TP53", "MTHFR", "CFTR", "APOE", "KRAS", "ALDH2"])
    chrom = st.selectbox("Chromosome Node Identifier", ["1", "7", "11", "17", "19"])
    position = st.number_input("Genomic Base Pair Position", min_value=1000000, max_value=150000000, value=43044295)
    ref_allele = st.selectbox("Reference Allele (Wild Type)", ["A", "C", "G", "T"])
    mut_allele = st.selectbox("Mutant Allele (Variant)", ["A", "C", "G", "T"])

with col2:
    st.subheader("🔮 Predicted Clinical Insight")
    
    # --- REAL-TIME FEATURE ENGINEERING ---
    # build empty row template initialized with zeros
    #input from user selectors will be received by this row
    input_row = pd.DataFrame(0, index=[0], columns=features)
    
    # Log-transforming genomic position entered by user
    if "log_genomic_position" in input_row.columns:
        input_row["log_genomic_position"] = np.log1p(position)
        
    # One-hot encoding input from user selectors
    if f"gene_id_{gene}" in input_row.columns: input_row[f"gene_id_{gene}"] = 1
    if f"chromosome_{chrom}" in input_row.columns: input_row[f"chromosome_{chrom}"] = 1
    if f"reference_allele_{ref_allele}" in input_row.columns: input_row[f"reference_allele_{ref_allele}"] = 1
    if f"mutant_allele_{mut_allele}" in input_row.columns: input_row[f"mutant_allele_{mut_allele}"] = 1
    
    # Run model prediction
    probabilities = model.predict_proba(input_row)[0]
    
    # Obtain predicted class and its probability
    predicted_class_idx = np.argmax(probabilities)
    predicted_label = target_map[predicted_class_idx]
    max_prob = probabilities[predicted_class_idx] * 100
    
    if predicted_label == "Benign":
        st.success(f"✅ Prediction Result: **{predicted_label} Variant Profile** ({max_prob:.1f}% Confidence)")
    elif predicted_label == "Pathogenic":
        st.error(f"🚨 Prediction Result: **{predicted_label} Mutation Flag** ({max_prob:.1f}% Confidence)")
    else:
        st.warning(f"⚠️ Prediction Result: **{predicted_label} Strain Detected** ({max_prob:.1f}% Confidence)")
        
    # Display probability for all categories
    st.write("")
    st.write("**Probability Matrix Metrics Distribution Output:**")
    for idx, label in target_map.items():
        st.progress(float(probabilities[idx]))
        st.write(f"🧬 {label}: {probabilities[idx]*100:.1f}%")

# ==========================================
#         FOOTER PORTFOLIO ANCHOR
# ==========================================
st.write("---")
st.caption(
    """
    Designed and engineered by **Dagoberto Venera-Ponton, PhD**.  
    Open-source code available on [GitHub](https://github.com/dagovenera/the-Genomic-Variant-Classifier.git).
    """
)