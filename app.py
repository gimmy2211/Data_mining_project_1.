from pathlib import Path
from typing import Dict

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "wholesale_customers.csv"
FEATURE_NAMES = [
    "Fresh", "Milk", "Grocery", "Frozen", "Detergents_Paper", "Delicassen"
]
TARGET_NAMES = {0: "Horeca", 1: "Retail"}


def train_pipeline() -> Pipeline:
    """Build the small model during a cold start; data has only 440 rows."""
    data = pd.read_csv(DATA_PATH)
    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=5000, random_state=42)),
        ]
    )
    pipeline.fit(data[FEATURE_NAMES], data["Channel"].map({1: 0, 2: 1}))
    return pipeline


pipeline = train_pipeline()

app = FastAPI(
    title="Wholesale Customer Channel API",
    description="Predicts whether a wholesale customer is Horeca or Retail.",
    version="1.0.0",
)


class PredictionInput(BaseModel):
    features: Dict[str, float]


@app.get("/")
def home():
    return {
        "message": "ML Prediction API is running",
        "docs": "/docs",
        "prediction_endpoint": "/predict",
        "required_features": FEATURE_NAMES,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: PredictionInput):
    received = payload.features
    missing = [name for name in FEATURE_NAMES if name not in received]
    extra = [name for name in received if name not in FEATURE_NAMES]
    if missing or extra:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Input features do not match the model requirements",
                "missing_features": missing,
                "unexpected_features": extra,
            },
        )

    input_frame = pd.DataFrame(
        [[received[name] for name in FEATURE_NAMES]], columns=FEATURE_NAMES
    )
    prediction = int(pipeline.predict(input_frame)[0])
    probabilities = pipeline.predict_proba(input_frame)[0]
    return {
        "prediction": TARGET_NAMES[prediction],
        "class_id": prediction,
        "probabilities": {
            TARGET_NAMES[int(class_id)]: round(float(probability), 4)
            for class_id, probability in zip(pipeline.classes_, probabilities)
        },
    }
