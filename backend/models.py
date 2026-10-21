"""
Disease and model performance endpoints.
GET /api/diseases
GET /api/model-performance
"""
import logging
from fastapi import APIRouter, HTTPException
from ml.model_utils import load_metrics

logger = logging.getLogger(__name__)
router = APIRouter()

DISEASES = [
    {
        "id": "heart",
        "name": "Heart Disease",
        "description": "Predicts the likelihood of heart disease based on clinical parameters.",
        "icon": "❤️",
        "features": [
            {"name": "age", "label": "Age", "type": "number", "unit": "years", "min": 1, "max": 120},
            {"name": "sex", "label": "Sex", "type": "select", "options": [{"value": 1, "label": "Male"}, {"value": 0, "label": "Female"}]},
            {"name": "cp", "label": "Chest Pain Type", "type": "select", "options": [
                {"value": 0, "label": "Typical Angina"}, {"value": 1, "label": "Atypical Angina"},
                {"value": 2, "label": "Non-anginal Pain"}, {"value": 3, "label": "Asymptomatic"}
            ]},
            {"name": "trestbps", "label": "Resting Blood Pressure", "type": "number", "unit": "mm Hg", "min": 50, "max": 250},
            {"name": "chol", "label": "Serum Cholesterol", "type": "number", "unit": "mg/dl", "min": 50, "max": 600},
            {"name": "fbs", "label": "Fasting Blood Sugar > 120 mg/dl", "type": "select", "options": [{"value": 1, "label": "True"}, {"value": 0, "label": "False"}]},
            {"name": "restecg", "label": "Resting ECG Results", "type": "select", "options": [
                {"value": 0, "label": "Normal"}, {"value": 1, "label": "ST-T Wave Abnormality"}, {"value": 2, "label": "Left Ventricular Hypertrophy"}
            ]},
            {"name": "thalach", "label": "Maximum Heart Rate Achieved", "type": "number", "unit": "bpm", "min": 50, "max": 250},
            {"name": "exang", "label": "Exercise Induced Angina", "type": "select", "options": [{"value": 1, "label": "Yes"}, {"value": 0, "label": "No"}]},
            {"name": "oldpeak", "label": "ST Depression (Exercise vs Rest)", "type": "number", "unit": "mm", "min": 0, "max": 10, "step": 0.1},
            {"name": "slope", "label": "Slope of Peak Exercise ST Segment", "type": "select", "options": [
                {"value": 0, "label": "Upsloping"}, {"value": 1, "label": "Flat"}, {"value": 2, "label": "Downsloping"}
            ]},
            {"name": "ca", "label": "Number of Major Vessels (Fluoroscopy)", "type": "select", "options": [
                {"value": 0, "label": "0"}, {"value": 1, "label": "1"}, {"value": 2, "label": "2"}, {"value": 3, "label": "3"}
            ]},
            {"name": "thal", "label": "Thalassemia", "type": "select", "options": [
                {"value": 1, "label": "Normal"}, {"value": 2, "label": "Fixed Defect"}, {"value": 3, "label": "Reversible Defect"}
            ]},
        ],
        "color": "#ef4444",
        "gradient": "from-red-500 to-rose-600",
    },
    {
        "id": "diabetes",
        "name": "Diabetes",
        "description": "Predicts the likelihood of diabetes using the Pima Indians Diabetes dataset.",
        "icon": "🩸",
        "features": [
            {"name": "Pregnancies", "label": "Number of Pregnancies", "type": "number", "unit": "count", "min": 0, "max": 20},
            {"name": "Glucose", "label": "Plasma Glucose Concentration", "type": "number", "unit": "mg/dL", "min": 0, "max": 300},
            {"name": "BloodPressure", "label": "Diastolic Blood Pressure", "type": "number", "unit": "mm Hg", "min": 0, "max": 150},
            {"name": "SkinThickness", "label": "Triceps Skin Fold Thickness", "type": "number", "unit": "mm", "min": 0, "max": 100},
            {"name": "Insulin", "label": "2-Hour Serum Insulin", "type": "number", "unit": "μU/mL", "min": 0, "max": 1000},
            {"name": "BMI", "label": "Body Mass Index (BMI)", "type": "number", "unit": "kg/m²", "min": 0, "max": 70, "step": 0.1},
            {"name": "DiabetesPedigreeFunction", "label": "Diabetes Pedigree Function", "type": "number", "unit": "score", "min": 0, "max": 3, "step": 0.001},
            {"name": "Age", "label": "Age", "type": "number", "unit": "years", "min": 1, "max": 120},
        ],
        "color": "#3b82f6",
        "gradient": "from-blue-500 to-cyan-500",
    },
    {
        "id": "breast_cancer",
        "name": "Breast Cancer",
        "description": "Predicts benign vs malignant classification using the Wisconsin Breast Cancer dataset.",
        "icon": "🎗️",
        "features": [
            {"name": "mean radius", "label": "Mean Radius", "type": "number", "min": 0, "max": 50, "step": 0.01},
            {"name": "mean texture", "label": "Mean Texture", "type": "number", "min": 0, "max": 50, "step": 0.01},
            {"name": "mean perimeter", "label": "Mean Perimeter", "type": "number", "min": 0, "max": 250, "step": 0.01},
            {"name": "mean area", "label": "Mean Area", "type": "number", "min": 0, "max": 3000, "step": 0.01},
            {"name": "mean smoothness", "label": "Mean Smoothness", "type": "number", "min": 0, "max": 1, "step": 0.0001},
            {"name": "mean compactness", "label": "Mean Compactness", "type": "number", "min": 0, "max": 1, "step": 0.0001},
            {"name": "mean concavity", "label": "Mean Concavity", "type": "number", "min": 0, "max": 1, "step": 0.0001},
            {"name": "mean concave points", "label": "Mean Concave Points", "type": "number", "min": 0, "max": 1, "step": 0.0001},
            {"name": "mean symmetry", "label": "Mean Symmetry", "type": "number", "min": 0, "max": 1, "step": 0.0001},
            {"name": "mean fractal dimension", "label": "Mean Fractal Dimension", "type": "number", "min": 0, "max": 1, "step": 0.0001},
            {"name": "radius error", "label": "Radius Error", "type": "number", "min": 0, "max": 5, "step": 0.001},
            {"name": "texture error", "label": "Texture Error", "type": "number", "min": 0, "max": 5, "step": 0.001},
            {"name": "perimeter error", "label": "Perimeter Error", "type": "number", "min": 0, "max": 30, "step": 0.01},
            {"name": "area error", "label": "Area Error", "type": "number", "min": 0, "max": 600, "step": 0.01},
            {"name": "smoothness error", "label": "Smoothness Error", "type": "number", "min": 0, "max": 0.05, "step": 0.00001},
            {"name": "compactness error", "label": "Compactness Error", "type": "number", "min": 0, "max": 0.2, "step": 0.0001},
            {"name": "concavity error", "label": "Concavity Error", "type": "number", "min": 0, "max": 0.5, "step": 0.0001},
            {"name": "concave points error", "label": "Concave Points Error", "type": "number", "min": 0, "max": 0.2, "step": 0.0001},
            {"name": "symmetry error", "label": "Symmetry Error", "type": "number", "min": 0, "max": 0.1, "step": 0.0001},
            {"name": "fractal dimension error", "label": "Fractal Dimension Error", "type": "number", "min": 0, "max": 0.05, "step": 0.00001},
            {"name": "worst radius", "label": "Worst Radius", "type": "number", "min": 0, "max": 50, "step": 0.01},
            {"name": "worst texture", "label": "Worst Texture", "type": "number", "min": 0, "max": 50, "step": 0.01},
            {"name": "worst perimeter", "label": "Worst Perimeter", "type": "number", "min": 0, "max": 300, "step": 0.01},
            {"name": "worst area", "label": "Worst Area", "type": "number", "min": 0, "max": 5000, "step": 0.01},
            {"name": "worst smoothness", "label": "Worst Smoothness", "type": "number", "min": 0, "max": 1, "step": 0.0001},
            {"name": "worst compactness", "label": "Worst Compactness", "type": "number", "min": 0, "max": 2, "step": 0.0001},
            {"name": "worst concavity", "label": "Worst Concavity", "type": "number", "min": 0, "max": 2, "step": 0.0001},
            {"name": "worst concave points", "label": "Worst Concave Points", "type": "number", "min": 0, "max": 1, "step": 0.0001},
            {"name": "worst symmetry", "label": "Worst Symmetry", "type": "number", "min": 0, "max": 1, "step": 0.0001},
            {"name": "worst fractal dimension", "label": "Worst Fractal Dimension", "type": "number", "min": 0, "max": 0.3, "step": 0.0001},
        ],
        "color": "#a855f7",
        "gradient": "from-purple-500 to-pink-500",
    },
]


@router.get("/diseases", tags=["Diseases"])
async def get_diseases():
    """Return the list of supported diseases with their input feature schemas."""
    return {"diseases": DISEASES}


@router.get("/model-performance", tags=["Performance"])
async def get_model_performance():
    """Return model evaluation metrics for all diseases."""
    performance = {}
    for disease_id in ["heart", "diabetes", "breast_cancer"]:
        try:
            metrics = load_metrics(disease_id)
            performance[disease_id] = metrics
        except Exception as e:
            logger.warning(f"Could not load metrics for {disease_id}: {e}")
            performance[disease_id] = {"error": "Metrics not available. Run train.py first."}

    return {"performance": performance}
