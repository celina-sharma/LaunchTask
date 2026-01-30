import pandas as pd
import numpy as np
import json
import joblib
from pathlib import Path
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
)
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "final.csv"
FEATURE_PATH = BASE_DIR / "features" / "feature_list.json"
MODELS_DIR = BASE_DIR / "models"
EVAL_DIR = BASE_DIR / "evaluation"

MODELS_DIR.mkdir(exist_ok=True)
EVAL_DIR.mkdir(exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)

# Feature preparation
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
df["Fare_Log"] = np.log1p(df["Fare"])
df = pd.get_dummies(df, columns=["Sex", "Embarked"], drop_first=True)

X = df.drop(columns=["Survived", "PassengerId", "Name", "Ticket"], errors="ignore")
y = df["Survived"]

# Use selected features
with open(FEATURE_PATH) as f:
    selected_features = json.load(f)

X = X[selected_features]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Models
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
    "XGBoost": XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        use_label_encoder=False,
        random_state=42
    ),
    "NeuralNetwork": MLPClassifier(max_iter=1000, random_state=42)
}

results = {}
best_roc = -1
best_model = None
best_model_name = None

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    print(f"\nTraining {name}...")

    # Cross-validated predictions
    y_pred = cross_val_predict(
        model, X_train, y_train,
        cv=5, method="predict"
    )

    y_proba = cross_val_predict(
        model, X_train, y_train,
        cv=5, method="predict_proba"
    )[:, 1]

    results[name] = {
        "accuracy": accuracy_score(y_train, y_pred),
        "precision": precision_score(y_train, y_pred),
        "recall": recall_score(y_train, y_pred),
        "f1_score": f1_score(y_train, y_pred),
        "roc_auc": roc_auc_score(y_train, y_proba)
    }

    if results[name]["roc_auc"] > best_roc:
        best_roc = results[name]["roc_auc"]
        best_model = model
        best_model_name = name


best_model.fit(X_train, y_train)

# Save model
joblib.dump(best_model, MODELS_DIR / "best_model.pkl")

# Save metrics
with open(EVAL_DIR / "metrics.json", "w") as f:
    json.dump(results, f, indent=4)

# Confusion matrix on test set
y_test_pred = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_test_pred)

disp = ConfusionMatrixDisplay(cm)
disp.plot()
plt.title(f"Best Model: {best_model_name}")
plt.savefig(EVAL_DIR / "confusion_matrix.png")
plt.close()

print("\nBest Model Selected:", best_model_name)
print("\nMetrics")
print(json.dumps(results, indent=4))
