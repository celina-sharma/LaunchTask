import pandas as pd
import numpy as np
import shap
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "final.csv"
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
OUTPUT_DIR = BASE_DIR / "evaluation"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)

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

X = df[FEATURES]

# load tuned model
model = joblib.load(MODEL_PATH)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

#shap summary plot
plt.figure()
shap.summary_plot(
    shap_values,
    X,
    show=False
)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "shap_summary.png")
plt.close()

print("SHAP summary plot saved successfully")
