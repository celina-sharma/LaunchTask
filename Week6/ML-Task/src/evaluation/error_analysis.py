import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "final.csv"
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
OUTPUT_PATH = BASE_DIR / "evaluation" / "error_heatmap.png"

# Load data
df = pd.read_csv(DATA_PATH)

# Feature engineering (same as training)
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

df = pd.get_dummies(
    df,
    columns=["Sex", "Embarked"],
    drop_first=True
)

FEATURES = [
    "Sex_male",
    "Fare",
    "Embarked_S",
    "Embarked_Q",
    "IsAlone",
    "Age",
    "SibSp",
    "Pclass"
]

X = df[FEATURES].fillna(0)
y = df["Survived"]

# Load model
model = joblib.load(MODEL_PATH)

# Predictions
df["predicted"] = model.predict(X)
df["error"] = df["predicted"] != df["Survived"]

# Bin Fare (important for heatmap readability)
df["Fare_bin"] = pd.qcut(df["Fare"], q=4, labels=["Low", "Mid", "High", "Very High"])

# Error rate by category
pivot = df.pivot_table(
    values="error",
    index="Pclass",
    columns="Fare_bin",
    aggfunc="mean",
    observed=False
)

# Plot heatmap
plt.figure(figsize=(8, 5))
sns.heatmap(
    pivot,
    annot=True,
    fmt=".2f",
    cmap="Reds"
)
plt.title("Error Rate Heatmap (by Class & Fare)")
plt.xlabel("Fare Category")
plt.ylabel("Passenger Class")
plt.tight_layout()
plt.savefig(OUTPUT_PATH)
plt.close()

print("Error analysis heatmap saved successfully.")
