"""
Reusable preprocessing pipelines for each disease dataset.
All preprocessing is encapsulated inside sklearn Pipelines to prevent data leakage.
"""
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


# ---------------------------------------------------------------------------
# Heart Disease (UCI Cleveland) feature config
# ---------------------------------------------------------------------------
HEART_FEATURES = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal"
]
HEART_TARGET = "target"

HEART_NUMERICAL = ["age", "trestbps", "chol", "thalach", "oldpeak"]
HEART_CATEGORICAL = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]

# ---------------------------------------------------------------------------
# Diabetes (Pima Indians) feature config
# ---------------------------------------------------------------------------
DIABETES_FEATURES = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]
DIABETES_TARGET = "Outcome"

DIABETES_NUMERICAL = DIABETES_FEATURES  # all numerical
DIABETES_CATEGORICAL = []

# Columns where 0 is physiologically impossible → treat as missing
DIABETES_ZERO_AS_NAN = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

# ---------------------------------------------------------------------------
# Breast Cancer (Wisconsin) feature config
# ---------------------------------------------------------------------------
# sklearn's load_breast_cancer provides 30 features
BREAST_CANCER_TARGET = "target"


# ---------------------------------------------------------------------------
# Builder functions
# ---------------------------------------------------------------------------

def build_heart_preprocessor():
    """ColumnTransformer for Heart Disease dataset."""
    numerical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    preprocessor = ColumnTransformer(transformers=[
        ("num", numerical_transformer, HEART_NUMERICAL),
        ("cat", categorical_transformer, HEART_CATEGORICAL),
    ], remainder="drop")
    return preprocessor


def build_diabetes_preprocessor():
    """ColumnTransformer for Diabetes dataset."""
    numerical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    preprocessor = ColumnTransformer(transformers=[
        ("num", numerical_transformer, DIABETES_NUMERICAL),
    ], remainder="drop")
    return preprocessor


def build_breast_cancer_preprocessor(feature_names: list):
    """ColumnTransformer for Breast Cancer dataset (all numerical)."""
    numerical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    preprocessor = ColumnTransformer(transformers=[
        ("num", numerical_transformer, feature_names),
    ], remainder="drop")
    return preprocessor


def preprocess_diabetes_zeros(df: pd.DataFrame) -> pd.DataFrame:
    """Replace physiologically impossible zeros with NaN for Diabetes dataset."""
    df = df.copy()
    for col in DIABETES_ZERO_AS_NAN:
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)
    return df


def get_disease_config(disease: str) -> dict:
    """Return feature/target config for a disease."""
    configs = {
        "heart": {
            "features": HEART_FEATURES,
            "target": HEART_TARGET,
            "numerical": HEART_NUMERICAL,
            "categorical": HEART_CATEGORICAL,
            "preprocessor_fn": build_heart_preprocessor,
        },
        "diabetes": {
            "features": DIABETES_FEATURES,
            "target": DIABETES_TARGET,
            "numerical": DIABETES_NUMERICAL,
            "categorical": DIABETES_CATEGORICAL,
            "preprocessor_fn": build_diabetes_preprocessor,
        },
        "breast_cancer": {
            "features": None,  # determined dynamically from dataset
            "target": BREAST_CANCER_TARGET,
            "numerical": None,
            "categorical": [],
            "preprocessor_fn": None,  # built dynamically
        },
    }
    return configs[disease]
