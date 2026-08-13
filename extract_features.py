import sqlite3
import pandas as pd
import numpy as np

print("⚙️ Launching Feature Extraction Engine...")

# 1. Connect to Relational Data Warehouse
conn = sqlite3.connect("genomics_warehouse.db")

# 2. Extract parsed records with custom SQL Query
# IMPORTANT: leave out primary key 'id' to prevent overfitting during model training
query = """
    SELECT gene_id, chromosome, position, reference_allele, mutant_allele, clinical_significance
    FROM mutations
"""
raw_data_df = pd.read_sql_query(query, conn)
conn.close()

print(f"📊 Recovered {len(raw_data_df)} records from SQL database for feature processing.")

# 3. Target Label Encoding
# Assign target categories to distinct integers for classifier model
target_map = {"Benign": 0, "Pathogenic": 1, "Drug-Resistant": 2}
y = raw_data_df["clinical_significance"].map(target_map)


# 4. FEATURE ENGINEERING (One-Hot Encoding)
# Machine Learning models can't read strings like "BRCA1" or "A".
# Moreover: we cannot simply assign their categories to distinct integers
# Why? Because the model may assumme that there is an order in the categories
# Thus, we must binarize them via One-Hot Encoding.
print("🔀 Transforming categorical features into numerically encoded columns...")

categorical_cols = ["gene_id", "chromosome", "reference_allele", "mutant_allele"]

# pd.get_dummies turns text strings into binary (0 and 1) one-hot encoded columns instantly
X_categorical = pd.get_dummies(raw_data_df[categorical_cols], dtype=int)

# Normalize position numerals with log-scale transformation
# This stops massive positional integer scales from overriding model gradients
X_numerical = pd.DataFrame({
    "log_genomic_position": np.log1p(raw_data_df["position"])
})

# Combine numerical and categorical features back together
X_final = pd.concat([X_numerical, X_categorical], axis=1)

# Add label-encoded target class to the matrix array
X_final["target"] = y

# 5. Export clean encoded data matrix for model training
output_csv = "MLready_features.csv"
X_final.to_csv(output_csv, index=False)

print("\n🔍 --- FEATURE SELECTION SUMMARY MATRIX ---")
print(f"Total Columns for Model Input: {X_final.shape[1] - 1} features")
print(f"Target Labels Configuration: {target_map}")
print(f"📁 Training data saved to: {output_csv}")
