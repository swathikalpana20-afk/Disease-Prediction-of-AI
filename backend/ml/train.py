"""
Training script for all three disease prediction models.

Usage:
    python backend/ml/train.py

This script:
1. Downloads/loads each public dataset
2. Validates and preprocesses data
3. Trains 4 classifiers per disease (LR, SVM, RF, XGBoost)
4. Evaluates each model on the test set
5. Selects the best model by F1 score
6. Saves the best model pipeline + evaluation metrics
7. Saves feature names for explainability

Datasets used:
- Heart Disease: UCI Heart Disease (Cleveland) via ucimlrepo or local CSV
- Diabetes: Pima Indians Diabetes via ucimlrepo or direct download
- Breast Cancer: sklearn's built-in Wisconsin Breast Cancer dataset
"""
import sys
import os
import json
import logging
import warnings
import numpy as np
import pandas as pd
from pathlib import Path

# Ensure backend/ is on the path when called as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.datasets import load_breast_cancer

from ml.preprocessing import (
    HEART_FEATURES, HEART_TARGET,
    DIABETES_FEATURES, DIABETES_TARGET, DIABETES_ZERO_AS_NAN,
    build_heart_preprocessor, build_diabetes_preprocessor, build_breast_cancer_preprocessor,
    preprocess_diabetes_zeros,
)
from ml.evaluate import evaluate_model, select_best_model, build_metrics_summary
from ml.model_utils import (
    save_model, save_best_model_name, save_metrics,
    save_feature_names, get_dataset_dir, get_model_dir
)

warnings.filterwarnings("ignore")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("train")

RANDOM_STATE = 42
TEST_SIZE = 0.2

CLASSIFIERS = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000, random_state=RANDOM_STATE, C=1.0
    ),
    "SVM": SVC(
        kernel="rbf", probability=True, random_state=RANDOM_STATE, C=1.0
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1
    ),
    "XGBoost": XGBClassifier(
        n_estimators=100, random_state=RANDOM_STATE,
        eval_metric="logloss", use_label_encoder=False,
        verbosity=0, n_jobs=-1
    ),
}


# ---------------------------------------------------------------------------
# Dataset loaders
# ---------------------------------------------------------------------------

def load_heart_dataset() -> pd.DataFrame:
    """Load Heart Disease dataset (UCI Cleveland via ucimlrepo or local CSV)."""
    dataset_dir = get_dataset_dir("heart")
    local_path = dataset_dir / "heart.csv"

    if local_path.exists():
        logger.info(f"Loading Heart Disease from local file: {local_path}")
        df = pd.read_csv(local_path)
    else:
        logger.info("Fetching Heart Disease dataset from ucimlrepo...")
        try:
            from ucimlrepo import fetch_ucirepo
            heart_disease = fetch_ucirepo(id=45)
            X = heart_disease.data.features
            y = heart_disease.data.targets
            df = pd.concat([X, y], axis=1)
            # Flatten multi-class target to binary (0 = no disease, 1 = disease)
            target_col = df.columns[-1]
            df[target_col] = (df[target_col] > 0).astype(int)
            df.columns = [c.lower().strip() for c in df.columns]
            # Standard Cleveland column names
            cols_map = {
                "age": "age", "sex": "sex", "cp": "cp",
                "trestbps": "trestbps", "chol": "chol", "fbs": "fbs",
                "restecg": "restecg", "thalach": "thalach", "exang": "exang",
                "oldpeak": "oldpeak", "slope": "slope", "ca": "ca",
                "thal": "thal", "num": "target",
            }
            df = df.rename(columns=cols_map)
            df.to_csv(local_path, index=False)
            logger.info(f"Saved Heart Disease dataset to {local_path}")
        except Exception as e:
            logger.warning(f"ucimlrepo failed: {e}. Trying direct download...")
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
            col_names = ["age","sex","cp","trestbps","chol","fbs","restecg",
                         "thalach","exang","oldpeak","slope","ca","thal","target"]
            try:
                import httpx
                import io
                response = httpx.get(url, follow_redirects=True, verify=True)
                response.raise_for_status()
                df = pd.read_csv(io.StringIO(response.text), header=None, names=col_names, na_values="?")
            except Exception as dl_e:
                logger.error(f"Download failed: {dl_e}. Please manually download {url} and save as {local_path}")
                raise dl_e
            
            df["target"] = (df["target"] > 0).astype(int)
            df.to_csv(local_path, index=False)
            logger.info(f"Saved Heart Disease dataset to {local_path}")

    # Validate required columns exist
    for col in HEART_FEATURES + [HEART_TARGET]:
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}' in Heart Disease dataset. Columns: {df.columns.tolist()}")

    # Replace '?' / invalid values
    df = df.replace("?", np.nan)
    for col in HEART_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    logger.info(f"Heart Disease dataset: {df.shape[0]} rows, {df.shape[1]} cols")
    return df


def load_diabetes_dataset() -> pd.DataFrame:
    """Load Pima Indians Diabetes dataset."""
    dataset_dir = get_dataset_dir("diabetes")
    local_path = dataset_dir / "diabetes.csv"

    if local_path.exists():
        logger.info(f"Loading Diabetes from local file: {local_path}")
        df = pd.read_csv(local_path)
    else:
        logger.info("Fetching Diabetes dataset from ucimlrepo...")
        try:
            from ucimlrepo import fetch_ucirepo
            pima = fetch_ucirepo(id=34)
            X = pima.data.features
            y = pima.data.targets
            df = pd.concat([X, y], axis=1)
            df.columns = [c.strip() for c in df.columns]
            # Normalise target column name
            target_col = [c for c in df.columns if c.lower() in ("class", "outcome", "diabetes")]
            if target_col:
                df = df.rename(columns={target_col[0]: "Outcome"})
            df.to_csv(local_path, index=False)
        except Exception as e:
            logger.warning(f"ucimlrepo failed: {e}. Trying direct download...")
            url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
            col_names = ["Pregnancies","Glucose","BloodPressure","SkinThickness",
                         "Insulin","BMI","DiabetesPedigreeFunction","Age","Outcome"]
            try:
                import httpx
                import io
                response = httpx.get(url, follow_redirects=True, verify=True)
                response.raise_for_status()
                df = pd.read_csv(io.StringIO(response.text), header=None, names=col_names)
            except Exception as dl_e:
                logger.error(f"Download failed: {dl_e}. Please manually download {url} and save as {local_path}")
                raise dl_e
            
            df.to_csv(local_path, index=False)
        logger.info(f"Saved Diabetes dataset to {local_path}")

    for col in DIABETES_FEATURES + [DIABETES_TARGET]:
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}' in Diabetes dataset. Columns: {df.columns.tolist()}")

    logger.info(f"Diabetes dataset: {df.shape[0]} rows, {df.shape[1]} cols")
    return df


def load_breast_cancer_dataset():
    """Load Wisconsin Breast Cancer dataset from sklearn."""
    logger.info("Loading Breast Cancer dataset from sklearn...")
    bc = load_breast_cancer()
    feature_names = [str(f) for f in bc.feature_names]
    df = pd.DataFrame(bc.data, columns=feature_names)
    df["target"] = bc.target
    # In sklearn: 0=malignant, 1=benign — keep as-is (target=1 means benign)
    logger.info(f"Breast Cancer dataset: {df.shape[0]} rows, {len(feature_names)} features")
    return df, feature_names


# ---------------------------------------------------------------------------
# Training functions
# ---------------------------------------------------------------------------

def train_disease(disease: str, X, y, preprocessor_fn, feature_names: list):
    """
    Train all classifiers for one disease, evaluate, select best, save.
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"Training models for: {disease.upper()}")
    logger.info(f"{'='*60}")

    # Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    logger.info(f"Train: {len(X_train)} | Test: {len(X_test)}")

    preprocessor = preprocessor_fn()
    all_metrics = []

    for clf_name, clf in CLASSIFIERS.items():
        logger.info(f"  Training {clf_name}...")
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf),
        ])
        pipeline.fit(X_train, y_train)
        metrics = evaluate_model(pipeline, X_test, y_test, clf_name)
        all_metrics.append(metrics)
        # Save every model (for comparison in UI)
        model_key = clf_name.lower().replace(" ", "_")
        save_model(pipeline, disease, model_key)

    best_name = select_best_model(all_metrics)
    best_key = best_name.lower().replace(" ", "_")
    save_best_model_name(disease, best_key)

    # Save consolidated metrics
    dataset_info = {
        "total_samples": int(len(X)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "n_features": int(X.shape[1]),
        "class_distribution": {
            "train": {str(k): int(v) for k, v in zip(*np.unique(y_train, return_counts=True))},
            "test": {str(k): int(v) for k, v in zip(*np.unique(y_test, return_counts=True))},
        },
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
    }
    summary = build_metrics_summary(disease, dataset_info, all_metrics, best_name)
    save_metrics(disease, summary)
    save_feature_names(disease, feature_names)

    logger.info(f"✓ Best model for {disease}: {best_name}")
    return summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    logger.info("Starting Disease Prediction Model Training")
    logger.info(f"Random state: {RANDOM_STATE} | Test size: {TEST_SIZE}")

    results = {}

    # --- Heart Disease ---
    df_heart = load_heart_dataset()
    X_heart = df_heart[HEART_FEATURES]
    y_heart = df_heart[HEART_TARGET].astype(int)
    results["heart"] = train_disease(
        "heart", X_heart, y_heart,
        build_heart_preprocessor, HEART_FEATURES
    )

    # --- Diabetes ---
    df_diabetes = load_diabetes_dataset()
    df_diabetes = preprocess_diabetes_zeros(df_diabetes)
    X_diabetes = df_diabetes[DIABETES_FEATURES]
    y_diabetes = df_diabetes[DIABETES_TARGET].astype(int)
    results["diabetes"] = train_disease(
        "diabetes", X_diabetes, y_diabetes,
        build_diabetes_preprocessor, DIABETES_FEATURES
    )

    # --- Breast Cancer ---
    df_bc, bc_features = load_breast_cancer_dataset()
    X_bc = df_bc[bc_features]
    y_bc = df_bc["target"].astype(int)
    results["breast_cancer"] = train_disease(
        "breast_cancer", X_bc, y_bc,
        lambda: build_breast_cancer_preprocessor(bc_features), bc_features
    )

    # Print summary table
    logger.info("\n" + "="*70)
    logger.info("TRAINING COMPLETE — SUMMARY")
    logger.info("="*70)
    header = f"{'Disease':<20} {'Best Model':<25} {'Accuracy':>9} {'F1':>9} {'AUC':>9}"
    logger.info(header)
    logger.info("-"*70)
    for disease, summary in results.items():
        best = next(m for m in summary["models"] if m["model"] == summary["best_model"])
        logger.info(
            f"{disease:<20} {summary['best_model']:<25} "
            f"{best['accuracy']:>9.4f} {best['f1_score']:>9.4f} {best['roc_auc']:>9.4f}"
        )
    logger.info("="*70)
    logger.info("All models saved successfully. You can now start the FastAPI server.")


if __name__ == "__main__":
    main()
