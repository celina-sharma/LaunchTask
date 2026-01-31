from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import uuid
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
LOG_FILE = BASE_DIR / "logs"/"prediction_logs.csv"
LOG_FILE.parent.mkdir(exist_ok=True)
#Load Model
model = joblib.load(MODEL_PATH)
MODEL_VERSION = "v1.0"

#Feature Order
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

#Logging Helper
def log_prediction(request_id, input_data, prediction, probability):
    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "request_id",
                "model_version",
                "input_data",
                "probability",
                "prediction"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            request_id,
            MODEL_VERSION,
            input_data,
            round(float(probability), 4),
            prediction
        ])

# FastApi App
app = FastAPI(
    title="Titanic Survival Prediction API",
    version="1.0"
)

@app.get("/")
def home():
    return {"message": "API is running successfully"}

#Input Schema
class PassengerInput(BaseModel):
    Sex_male: int = Field(..., ge=0, le=1, example=0)
    Fare: float = Field(..., ge=0, le=1000, example=32.2)
    Embarked_S: int = Field(..., ge=0, le=1)
    Embarked_Q: int = Field(..., ge=0, le=1)
    IsAlone: int = Field(..., ge=0, le=1)
    Age: int = Field(..., ge=0, le=100, example=28)
    SibSp: int = Field(..., ge=0, le=10)
    Pclass: int = Field(..., ge=1, le=3)


#Predict Endpoint
@app.post("/predict")
def predict(data: PassengerInput):
    request_id = str(uuid.uuid4())

    df = pd.DataFrame([data.dict()])[FEATURES]

    proba = model.predict_proba(df)[0][1]
    prediction = int(proba >= 0.5)

    log_prediction(
        request_id=request_id,
        input_data=data.dict(),
        prediction=prediction,
        probability=proba
    )

    return {
        "request_id": request_id,
        "model_version": MODEL_VERSION,
        "prediction": prediction,
        "probability": round(float(proba), 4)
    }
