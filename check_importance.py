import joblib
import pandas as pd

# Load trained model
model = joblib.load("fraud_model.pkl")

# Get feature names
try:
    feature_names = model.feature_names_in_
except:
    # If model doesn't store names, create manually
    feature_names = [f"Feature_{i}" for i in range(model.n_features_in_)]

# Get importance values
importances = model.feature_importances_

# Create DataFrame for clean view
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})

# Sort by importance (highest first)
importance_df = importance_df.sort_values(by="Importance", ascending=False)

print("\n=== Feature Importance Ranking ===\n")
print(importance_df)