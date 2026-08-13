import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from xgboost import XGBClassifier

print("🚀 Launching XGboost Training Engine...")

# 1. Load engineered ML matrix
df = pd.read_csv("MLready_features.csv")

# Separate features from target
X = df.drop(columns=["target"])
y = df["target"].astype(int)

feature_columns = X.columns.tolist()

# 2. Stratified Split to guarantee proportional representation of target classes
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

# 3. Initialize and Train XGBoost Classifier
model = XGBClassifier(
    n_estimators=120,
    max_depth=4,
    learning_rate=0.08,
    objective="multi:softprob", #outputs probability scores for all three target tags
    num_class=3,
    random_state=42,
    eval_metric="mlogloss"
)

print("🏋️ Training gradient boosting trees...")
model.fit(X_train, y_train)

# 4. Metrics Evaluation
print("\n📊 --- BIOINFORMATICS MODEL METRICS --- 📊\n")
y_pred = model.predict(X_val)
y_pred_proba = model.predict_proba(X_val)

target_names = ["Benign", "Pathogenic", "Drug-Resistant"]
print("1. Classification Report:")
print(classification_report(y_val, y_pred, target_names=target_names))

auc_score = roc_auc_score(y_val, y_pred_proba, multi_class="ovr")
print(f"\n2. ROC-AUC Score: {auc_score:.4f}")

print("\n3. Confusion Matrix Grid:")
print(confusion_matrix(y_val, y_pred))

# 5. Save the trained model alongside feature array and target map
print("\n💾 Archiving model, features and target encoding...")
genomic_artifacts = {
    "model": model,
    "features": feature_columns,
    "target_map": {0: "Benign", 1: "Pathogenic", 2: "Drug-Resistant"}
}
joblib.dump(genomic_artifacts, "XGboost_model.pkl")
print("🎉 Success! XGboost artifacts saved as: XGboost_model.pkl")
