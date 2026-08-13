# the-Genomic-Variant-Claffifier
End-to-end bioinformatics data pipeline utilizing Perl for parsing genomic variant call files (VCF), SQL for tracking mutations in a relational database, and Python Machine Learning for clinical trait classification

# 🧬 Genomic Variant Data Ingestion &  Processing Pipeline

[![RF App Live](https://shields.io)](https://the-genomic-variant-classifier-randforest.streamlit.app/)
[![XGB App Live](https://shields.io)](https://the-genomic-variant-classifier-xgboost.streamlit.app/)
[![Perl](https://shields.io)](https://perl.org)
[![SQL](https://shields.io)](https://sqlite.org)

A comprehensive bioinformatics framework designed to ingest Variant Call Format (VCF) genetic matrices, archive them within an SQL relational database, and train two machine learning classifiers to forescast the clinical significance of new, undiscovered, variants.

---

## 📊 The Production Architecture

To replicate an enterprise deployment evaluation, this pipeline outputs and serves two distinct production models that forescast clinical traits on new genetic variants with user-inputted features, one-hot encoded in the backend:


### 🏎️ Architectural Breakdowns
1. **Ingestion Engine (`parse_VCF_genomics.pl`):** A high-speed, memory-efficient **Perl** script that processes raw variant call format (VCF) data. It bypasses metadata noise, runs quality control checks to drop low-grade rows, and transforms messy text blocks into structured analytical formats.
2. **Relational Warehouse (`build_genomics_db.py`):** Ingests clean data structures into an indexed **SQL** storage grid.
3. **Feature Preprocessing (`extract_features.py`):** Translates biological string variables (Gene IDs and Alleles) into numeric matrices via automated **One-Hot-Encoding** and transforms the wide coordinate system of base-pair positions via logarithmic distribution formatting.
4. **The Champion-Challenger Classifiers (`train_genomics_RandForest.py`):** Trains a random forest classifier to predict multi-class clinical traits (Benign, Pathogenic, Drug-Resistant) from genetic variant features.
(`train_genomics_XGboost.py`):** Trains an extreme gradient booster classifier to predict multi-class clinical traits (Benign, Pathogenic, Drug-Resistant) from genetic variant features.
5. **Interactive Forecasting Deployment (`app_RandForest.py`):** A fully responsive web interface built with Streamlit, allowing stakeholders to dynamically devise genetic variants via slider to predict, with a random forest classifier, whether they are Benign, Pathogenic, or Drug-Resistant.
(`app_XGboost.py`):** A fully responsive web interface built with Streamlit, allowing stakeholders to dynamically devise genetic variants via slider to predict, with an extreme gradient booster classifier, whether they are Benign, Pathogenic, or Drug-Resistant.

---

## 🛠️ Unified Technical Stack

- **Languages:** Perl (Ingestion Engine), SQL (Relational Database Construction), Python (Database Retrieval & Feature Engineering)
- **Machine Learning Architecture:** Scikit-Learn (Random Forest Bagging), XGBoost (Gradient Boosting Trees)
- **Preprocessing:** Categorical Binarization/One-Hot Encoding
- **Metrics:** Multiclass Log-Loss Evaluation, Area Under the Receiver Operating Characteristic Curve (ROC-AUC)
- **Deployment Interface:** Streamlit Cloud Host Automation

---

## 🧪 Simulation Framework

To guarantee continuous development velocity, this project features a mock data generator that allowed to create all the pipeline before data were obtained from major genomic databases.

This simulation engine (`generate_raw_genomics_data.py`) was custom-built using Numpy and Pandas to generate synthetic genetic matrices in Variant Call Format (VCF). These synthetic matrices include low-grade data that must be detected and removed by the ingestion engine (`parse_VCF_genomics.pl`). This framework successfully streamlined local pipeline construction with realistic testing before scaling up to real data sources.

---

## 🚀 Execution & Local Deployment

```bash
# 1. Clone the environment infrastructure
git clone https://github.com
cd the-Genomic-Variant-Classifier

# 2. Optional: generate mock data if you do not have real data for genetic matrices in Variant Call Format (VCF)

# 3. Run high-speed data ingestion & feature engineering loop
python generate_raw_genomics_data.py
perl parse_genomics.pl
python build_genomics_db.py
python extract_features.py

# 4. Train both model weights simultaneously
python train_genomics_RandForest.py
python train_genomics_XGboost.py

# 5. Spin up either benchmark application dashboard interface
streamlit run app_random_forest.py
# OR: streamlit run app_xgboost.py
```

---

## 👨‍💻 Developer Profile
**Dagoberto Venera-Ponton, PhD**  
*Bioinformatics, Ecology, Advanced Statistical Modelling & Distributed Tech Pipelines*  
- **LinkedIn:** [[Link](https://linkedin.com/in/dagoberto-venera-ponton-phd)] | **Email:** [dagovenera@gmail.com]