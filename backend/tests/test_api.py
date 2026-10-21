"""
Backend API tests using pytest + httpx TestClient.
Run: cd backend && pytest tests/ -v
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

def test_health_endpoint():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


# ---------------------------------------------------------------------------
# Diseases endpoint
# ---------------------------------------------------------------------------

def test_get_diseases():
    resp = client.get("/api/diseases")
    assert resp.status_code == 200
    data = resp.json()
    assert "diseases" in data
    assert len(data["diseases"]) == 3
    ids = [d["id"] for d in data["diseases"]]
    assert "heart" in ids
    assert "diabetes" in ids
    assert "breast_cancer" in ids


# ---------------------------------------------------------------------------
# Prediction history
# ---------------------------------------------------------------------------

def test_prediction_history():
    resp = client.get("/api/prediction-history")
    assert resp.status_code == 200
    data = resp.json()
    assert "history" in data
    assert "count" in data


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def test_heart_prediction_invalid_age():
    """Age out of range should return 422."""
    payload = {
        "age": -5, "sex": 1, "cp": 0, "trestbps": 125, "chol": 212,
        "fbs": 0, "restecg": 1, "thalach": 168, "exang": 0,
        "oldpeak": 1.0, "slope": 2, "ca": 2, "thal": 3
    }
    resp = client.post("/api/predict/heart", json=payload)
    assert resp.status_code == 422


def test_heart_prediction_missing_field():
    """Missing required field should return 422."""
    payload = {"age": 52, "sex": 1}  # Missing most fields
    resp = client.post("/api/predict/heart", json=payload)
    assert resp.status_code == 422


def test_diabetes_prediction_invalid_glucose():
    """Glucose > 300 should return 422."""
    payload = {
        "Pregnancies": 2, "Glucose": 999, "BloodPressure": 62,
        "SkinThickness": 35, "Insulin": 0, "BMI": 33.6,
        "DiabetesPedigreeFunction": 0.627, "Age": 47
    }
    resp = client.post("/api/predict/diabetes", json=payload)
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Prediction endpoints (only run if models are trained)
# ---------------------------------------------------------------------------

HEART_SAMPLE = {
    "age": 52, "sex": 1, "cp": 0, "trestbps": 125, "chol": 212,
    "fbs": 0, "restecg": 1, "thalach": 168, "exang": 0,
    "oldpeak": 1.0, "slope": 2, "ca": 2, "thal": 3
}
DIABETES_SAMPLE = {
    "Pregnancies": 2, "Glucose": 138, "BloodPressure": 62,
    "SkinThickness": 35, "Insulin": 0, "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627, "Age": 47
}


def models_exist(disease: str) -> bool:
    model_dir = Path(__file__).parent.parent / "models" / disease
    return (model_dir / "best_model.json").exists()


@pytest.mark.skipif(not models_exist("heart"), reason="Heart models not trained")
def test_heart_prediction_success():
    resp = client.post("/api/predict/heart", json=HEART_SAMPLE)
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data
    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0
    assert "disclaimer" in data
    assert "feature_importance" in data


@pytest.mark.skipif(not models_exist("diabetes"), reason="Diabetes models not trained")
def test_diabetes_prediction_success():
    resp = client.post("/api/predict/diabetes", json=DIABETES_SAMPLE)
    assert resp.status_code == 200
    data = resp.json()
    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0
