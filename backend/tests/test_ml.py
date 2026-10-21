"""
ML pipeline tests: dataset loading, preprocessing, prediction shape.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer

from ml.preprocessing import (
    HEART_FEATURES, DIABETES_FEATURES,
    build_heart_preprocessor, build_diabetes_preprocessor,
    build_breast_cancer_preprocessor, preprocess_diabetes_zeros,
    DIABETES_ZERO_AS_NAN,
)
from ml.evaluate import evaluate_model, select_best_model


# ---------------------------------------------------------------------------
# Preprocessing tests
# ---------------------------------------------------------------------------

def test_diabetes_zero_replacement():
    """Zeros in physiologically-impossible columns should become NaN."""
    df = pd.DataFrame([{col: 0 for col in DIABETES_FEATURES}])
    df["Outcome"] = 0
    result = preprocess_diabetes_zeros(df)
    for col in DIABETES_ZERO_AS_NAN:
        assert pd.isna(result[col].iloc[0]), f"Expected NaN in {col}"


def test_heart_preprocessor_output_shape():
    """Heart preprocessor should produce a 2D array."""
    n = 10
    data = {
        "age": np.random.uniform(30, 80, n),
        "sex": np.random.randint(0, 2, n),
        "cp": np.random.randint(0, 4, n),
        "trestbps": np.random.uniform(80, 200, n),
        "chol": np.random.uniform(100, 400, n),
        "fbs": np.random.randint(0, 2, n),
        "restecg": np.random.randint(0, 3, n),
        "thalach": np.random.uniform(60, 200, n),
        "exang": np.random.randint(0, 2, n),
        "oldpeak": np.random.uniform(0, 5, n),
        "slope": np.random.randint(0, 3, n),
        "ca": np.random.randint(0, 4, n),
        "thal": np.random.randint(1, 4, n),
    }
    df = pd.DataFrame(data)
    preprocessor = build_heart_preprocessor()
    X_transformed = preprocessor.fit_transform(df)
    assert X_transformed.ndim == 2
    assert X_transformed.shape[0] == n


def test_diabetes_preprocessor_output_shape():
    n = 10
    data = {col: np.random.uniform(0, 100, n) for col in DIABETES_FEATURES}
    df = pd.DataFrame(data)
    preprocessor = build_diabetes_preprocessor()
    X_transformed = preprocessor.fit_transform(df)
    assert X_transformed.ndim == 2
    assert X_transformed.shape[0] == n


def test_breast_cancer_preprocessor():
    bc = load_breast_cancer()
    feature_names = list(bc.feature_names)
    df = pd.DataFrame(bc.data, columns=feature_names)
    preprocessor = build_breast_cancer_preprocessor(feature_names)
    X_transformed = preprocessor.fit_transform(df)
    assert X_transformed.shape[0] == df.shape[0]
    assert X_transformed.shape[1] == len(feature_names)


# ---------------------------------------------------------------------------
# Evaluate tests
# ---------------------------------------------------------------------------

def test_select_best_model_by_f1():
    metrics = [
        {"model": "A", "f1_score": 0.75, "accuracy": 0.90},
        {"model": "B", "f1_score": 0.85, "accuracy": 0.80},
        {"model": "C", "f1_score": 0.70, "accuracy": 0.95},
    ]
    best = select_best_model(metrics)
    assert best == "B", "Should select by F1, not accuracy"


# ---------------------------------------------------------------------------
# Dataset loading (integration, skipped if no internet)
# ---------------------------------------------------------------------------

def test_breast_cancer_dataset_loads():
    bc = load_breast_cancer()
    assert bc.data.shape[1] == 30
    assert len(bc.target_names) == 2
