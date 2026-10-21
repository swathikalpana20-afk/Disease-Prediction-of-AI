"""
Prediction endpoints.
POST /api/predict/heart
POST /api/predict/diabetes
POST /api/predict/breast-cancer
"""
import logging
from datetime import datetime
from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from ml.predict import predict_disease
from database.database import get_db, save_prediction

logger = logging.getLogger(__name__)
router = APIRouter()


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class HeartPredictionRequest(BaseModel):
    age: float = Field(..., ge=1, le=120, description="Age in years")
    sex: float = Field(..., ge=0, le=1, description="0=Female, 1=Male")
    cp: float = Field(..., ge=0, le=3, description="Chest pain type (0-3)")
    trestbps: float = Field(..., ge=50, le=250, description="Resting blood pressure (mm Hg)")
    chol: float = Field(..., ge=50, le=600, description="Serum cholesterol (mg/dl)")
    fbs: float = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl (0/1)")
    restecg: float = Field(..., ge=0, le=2, description="Resting ECG (0-2)")
    thalach: float = Field(..., ge=50, le=250, description="Maximum heart rate achieved (bpm)")
    exang: float = Field(..., ge=0, le=1, description="Exercise induced angina (0/1)")
    oldpeak: float = Field(..., ge=0, le=10, description="ST depression (mm)")
    slope: float = Field(..., ge=0, le=2, description="Slope of peak exercise ST segment (0-2)")
    ca: float = Field(..., ge=0, le=3, description="Number of major vessels (0-3)")
    thal: float = Field(..., ge=1, le=3, description="Thalassemia (1=normal, 2=fixed, 3=reversible)")

    model_config = {"json_schema_extra": {"example": {
        "age": 52, "sex": 1, "cp": 0, "trestbps": 125, "chol": 212,
        "fbs": 0, "restecg": 1, "thalach": 168, "exang": 0,
        "oldpeak": 1.0, "slope": 2, "ca": 2, "thal": 3
    }}}


class DiabetesPredictionRequest(BaseModel):
    Pregnancies: float = Field(..., ge=0, le=20)
    Glucose: float = Field(..., ge=0, le=300, description="Plasma glucose (mg/dL)")
    BloodPressure: float = Field(..., ge=0, le=150, description="Diastolic BP (mm Hg)")
    SkinThickness: float = Field(..., ge=0, le=100, description="Triceps skinfold (mm)")
    Insulin: float = Field(..., ge=0, le=1000, description="2-Hour serum insulin (μU/mL)")
    BMI: float = Field(..., ge=0, le=70, description="Body mass index (kg/m²)")
    DiabetesPedigreeFunction: float = Field(..., ge=0, le=3)
    Age: float = Field(..., ge=1, le=120)

    model_config = {"json_schema_extra": {"example": {
        "Pregnancies": 2, "Glucose": 138, "BloodPressure": 62,
        "SkinThickness": 35, "Insulin": 0, "BMI": 33.6,
        "DiabetesPedigreeFunction": 0.627, "Age": 47
    }}}


class BreastCancerPredictionRequest(BaseModel):
    mean_radius: float = Field(..., alias="mean radius", ge=0)
    mean_texture: float = Field(..., alias="mean texture", ge=0)
    mean_perimeter: float = Field(..., alias="mean perimeter", ge=0)
    mean_area: float = Field(..., alias="mean area", ge=0)
    mean_smoothness: float = Field(..., alias="mean smoothness", ge=0)
    mean_compactness: float = Field(..., alias="mean compactness", ge=0)
    mean_concavity: float = Field(..., alias="mean concavity", ge=0)
    mean_concave_points: float = Field(..., alias="mean concave points", ge=0)
    mean_symmetry: float = Field(..., alias="mean symmetry", ge=0)
    mean_fractal_dimension: float = Field(..., alias="mean fractal dimension", ge=0)
    radius_error: float = Field(..., alias="radius error", ge=0)
    texture_error: float = Field(..., alias="texture error", ge=0)
    perimeter_error: float = Field(..., alias="perimeter error", ge=0)
    area_error: float = Field(..., alias="area error", ge=0)
    smoothness_error: float = Field(..., alias="smoothness error", ge=0)
    compactness_error: float = Field(..., alias="compactness error", ge=0)
    concavity_error: float = Field(..., alias="concavity error", ge=0)
    concave_points_error: float = Field(..., alias="concave points error", ge=0)
    symmetry_error: float = Field(..., alias="symmetry error", ge=0)
    fractal_dimension_error: float = Field(..., alias="fractal dimension error", ge=0)
    worst_radius: float = Field(..., alias="worst radius", ge=0)
    worst_texture: float = Field(..., alias="worst texture", ge=0)
    worst_perimeter: float = Field(..., alias="worst perimeter", ge=0)
    worst_area: float = Field(..., alias="worst area", ge=0)
    worst_smoothness: float = Field(..., alias="worst smoothness", ge=0)
    worst_compactness: float = Field(..., alias="worst compactness", ge=0)
    worst_concavity: float = Field(..., alias="worst concavity", ge=0)
    worst_concave_points: float = Field(..., alias="worst concave points", ge=0)
    worst_symmetry: float = Field(..., alias="worst symmetry", ge=0)
    worst_fractal_dimension: float = Field(..., alias="worst fractal dimension", ge=0)

    model_config = {"populate_by_name": True}


# ---------------------------------------------------------------------------
# Response schema
# ---------------------------------------------------------------------------

class PredictionResponse(BaseModel):
    disease: str
    model_name: str
    prediction: int
    probability: float
    result_label: str
    explanation: str
    feature_importance: Dict[str, float]
    timestamp: str
    disclaimer: str = (
        "Educational purpose only. This prediction is NOT a medical diagnosis. "
        "Please consult a qualified healthcare professional for medical advice."
    )


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _run_prediction(disease: str, input_data: dict, db: Session) -> PredictionResponse:
    try:
        result = predict_disease(disease, input_data)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error for {disease}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed. Please try again.")

    try:
        save_prediction(db, result)
    except Exception as e:
        logger.warning(f"Failed to save prediction history: {e}")

    return PredictionResponse(
        **result,
        timestamp=datetime.utcnow().isoformat(),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/predict/heart", response_model=PredictionResponse, tags=["Predictions"])
async def predict_heart(request: HeartPredictionRequest, db: Session = Depends(get_db)):
    """
    Predict likelihood of heart disease.

    **Disclaimer**: For educational/demonstration purposes only.
    Not a medical diagnosis.
    """
    return _run_prediction("heart", request.model_dump(), db)


@router.post("/predict/diabetes", response_model=PredictionResponse, tags=["Predictions"])
async def predict_diabetes(request: DiabetesPredictionRequest, db: Session = Depends(get_db)):
    """
    Predict likelihood of diabetes.

    **Disclaimer**: For educational/demonstration purposes only.
    Not a medical diagnosis.
    """
    return _run_prediction("diabetes", request.model_dump(), db)


@router.post("/predict/breast-cancer", response_model=PredictionResponse, tags=["Predictions"])
async def predict_breast_cancer(
    request: BreastCancerPredictionRequest, db: Session = Depends(get_db)
):
    """
    Predict benign vs malignant (Wisconsin Breast Cancer dataset).

    **Disclaimer**: For educational/demonstration purposes only.
    Not a medical diagnosis.
    """
    # Convert aliased model to original feature names (with spaces)
    data = request.model_dump(by_alias=True)
    return _run_prediction("breast_cancer", data, db)
