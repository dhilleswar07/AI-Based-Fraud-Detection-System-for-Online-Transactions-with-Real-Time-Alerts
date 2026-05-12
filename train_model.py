from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib

print("Loading dataset...")

df = pd.read_csv("creditcard.csv")

print("Dataset Loaded ✅")
print("Shape:", df.shape)

# -----------------------------
# FEATURES & TARGET
# -----------------------------
X = df.drop("Class", axis=1)
y = df["Class"]

# -----------------------------
# TRAIN-TEST SPLIT
# -----------------------------
print("Splitting data...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    stratify=y,
    random_state=42
)

# -----------------------------
# SCALING
# -----------------------------
print("Scaling data...")

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -----------------------------
# MODEL TRAINING
# -----------------------------
print("Training Random Forest Model...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -----------------------------
# PREDICTIONS
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# METRICS
# -----------------------------
accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)
precision = round(precision_score(y_test, y_pred, zero_division=0) * 100, 2)
recall = round(recall_score(y_test, y_pred, zero_division=0) * 100, 2)
f1 = round(f1_score(y_test, y_pred, zero_division=0) * 100, 2)
cm = confusion_matrix(y_test, y_pred)

print("\n==============================")
print("Model Performance Metrics")
print("==============================")
print(f"Accuracy  : {accuracy}%")
print(f"Precision : {precision}%")
print(f"Recall    : {recall}%")
print(f"F1 Score  : {f1}%")
print("\nConfusion Matrix:")
print(cm)

print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# SAVE METRICS
# -----------------------------
metrics = {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "confusion_matrix": cm.tolist()
}

joblib.dump(metrics, "model_metrics.pkl")

# -----------------------------
# SAVE MODEL & SCALER
# -----------------------------
joblib.dump(model, "fraud_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\nModel trained and saved successfully ✅")