import pandas as pd
import ast
from scipy.stats import ks_2samp
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]

TRAIN_PATH = BASE_DIR / "data" / "processed" / "final.csv"
LOG_PATH = BASE_DIR / "logs" / "prediction_logs.csv"

train_df = pd.read_csv(TRAIN_PATH)
logs_df = pd.read_csv(LOG_PATH)

def safe_parse(x):
    try:
        return ast.literal_eval(x)
    except Exception:
        return None

inputs_df = (
    logs_df["input_data"]
    .apply(safe_parse)
    .dropna()
    .apply(pd.Series)
)

FEATURES = ["Age", "Fare", "Pclass"]

drift_report = {}

for feature in FEATURES:
    stat, p_value = ks_2samp(
        train_df[feature].dropna(),
        inputs_df[feature].dropna()
    )

    drift_report[feature] = {
        "p_value": round(float(p_value), 5),
        "drift_detected": bool(p_value < 0.05)
    }

OUTPUT_DIR = BASE_DIR / "monitoring"
OUTPUT_DIR.mkdir(exist_ok=True)

with open(OUTPUT_DIR / "drift_report.json", "w") as f:
    json.dump(drift_report, f, indent=4)

print("Drift analysis completed")
print(json.dumps(drift_report, indent=4))
