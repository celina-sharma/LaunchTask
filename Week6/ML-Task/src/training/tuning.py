import json
import optuna
import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "final.csv"
TUNING_DIR = BASE_DIR / "tuning"
MODELS_DIR = BASE_DIR / "models"

TUNING_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)


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
y = df["Survived"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# Objective function for Optuna
def objective(trial):

    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 300),
        "max_depth": trial.suggest_int("max_depth", 3, 8),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "random_state": 42
    }

    model = XGBClassifier(**params)
    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_proba)

    return roc_auc


# Run Optuna study
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=30)

best_params = study.best_params
best_score = study.best_value

# Train final model using best params
best_model = XGBClassifier(
    **best_params,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42
)

best_model.fit(X_train, y_train)

# Save tuned model
joblib.dump(best_model, MODELS_DIR / "best_model_tuned.pkl")

# Save tuning results
results = {
    "best_params": best_params,
    "best_roc_auc": best_score,
    "n_trials": len(study.trials)
}

with open(TUNING_DIR / "results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Optuna hyperparameter tuning completed")
print("Best ROC-AUC:", best_score)
print("Best Parameters:", best_params)
