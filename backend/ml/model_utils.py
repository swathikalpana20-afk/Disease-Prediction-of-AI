"""
Model utilities: save/load models, dataset downloading, path helpers.
"""
import os
import json
import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Project root = backend/
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATASETS_DIR = BASE_DIR / "datasets"
METRICS_DIR = BASE_DIR / "models"


def get_model_dir(disease: str) -> Path:
    """Return path to saved model directory for a disease."""
    d = MODELS_DIR / disease
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_dataset_dir(disease: str) -> Path:
    d = DATASETS_DIR / disease
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_model(pipeline, disease: str, model_name: str) -> Path:
    """Save a trained sklearn Pipeline with joblib."""
    path = get_model_dir(disease) / f"{model_name}.joblib"
    joblib.dump(pipeline, path)
    logger.info(f"Saved model: {path}")
    return path


def load_model(disease: str, model_name: str):
    """Load a saved sklearn Pipeline."""
    path = get_model_dir(disease) / f"{model_name}.joblib"
    if not path.exists():
        raise FileNotFoundError(f"Model not found: {path}. Run train.py first.")
    return joblib.load(path)


def save_best_model_name(disease: str, model_name: str):
    """Persist the name of the best model for a disease."""
    path = get_model_dir(disease) / "best_model.json"
    with open(path, "w") as f:
        json.dump({"best_model": model_name}, f)


def load_best_model_name(disease: str) -> str:
    path = get_model_dir(disease) / "best_model.json"
    if not path.exists():
        raise FileNotFoundError(f"best_model.json not found for {disease}. Run train.py first.")
    with open(path) as f:
        return json.load(f)["best_model"]


def load_best_model(disease: str):
    """Load the best model pipeline for a disease."""
    model_name = load_best_model_name(disease)
    return load_model(disease, model_name), model_name


def save_metrics(disease: str, metrics: dict):
    """Save evaluation metrics as JSON."""
    path = get_model_dir(disease) / "metrics.json"
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"Saved metrics: {path}")


def load_metrics(disease: str) -> dict:
    path = get_model_dir(disease) / "metrics.json"
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def load_feature_names(disease: str) -> list:
    path = get_model_dir(disease) / "feature_names.json"
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)


def save_feature_names(disease: str, feature_names: list):
    path = get_model_dir(disease) / "feature_names.json"
    with open(path, "w") as f:
        json.dump(feature_names, f)
