"""
Prediction module: loads best model, runs inference, computes SHAP explanations.
"""
import sys
import logging
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml.model_utils import load_best_model, load_feature_names
from ml.preprocessing import HEART_FEATURES, DIABETES_FEATURES

logger = logging.getLogger(__name__)


def _get_shap_values(pipeline, X_df: pd.DataFrame, feature_names: list) -> dict:
    """
    Compute SHAP values for tree-based models, fallback to feature coefficients
    for linear models (LR) or return None for SVM.
    Returns a dict: {feature_name: shap_value} sorted by abs importance.
    """
    try:
        import shap
        clf = pipeline.named_steps["classifier"]
        preprocessor = pipeline.named_steps["preprocessor"]
        X_transformed = preprocessor.transform(X_df)

        clf_type = type(clf).__name__

        if clf_type in ("RandomForestClassifier", "XGBClassifier",
                        "GradientBoostingClassifier", "ExtraTreesClassifier"):
            explainer = shap.TreeExplainer(clf)
            shap_vals = explainer.shap_values(X_transformed)
            # For binary: shap_values is [neg_class, pos_class] for RF
            if isinstance(shap_vals, list) and len(shap_vals) == 2:
                shap_vals = shap_vals[1]
            shap_vals = np.array(shap_vals).flatten()
        elif clf_type == "LogisticRegression":
            coef = clf.coef_[0]
            shap_vals = coef * X_transformed[0]
        else:
            # SVM or others: use decision function-based approximation
            return {}

        # Map back to original feature names (best-effort)
        n = min(len(feature_names), len(shap_vals))
        importance = {feature_names[i]: round(float(shap_vals[i]), 4) for i in range(n)}
        # Sort by absolute value
        importance = dict(sorted(importance.items(), key=lambda x: abs(x[1]), reverse=True))
        return importance

    except Exception as e:
        logger.warning(f"SHAP computation failed: {e}")
        return {}


def predict_disease(disease: str, input_data: dict) -> dict:
    """
    Run prediction for a disease.

    Args:
        disease: one of 'heart', 'diabetes', 'breast_cancer'
        input_data: dict mapping feature names to values

    Returns:
        {
            'disease': str,
            'model_name': str,
            'prediction': int,         # 0 or 1
            'probability': float,      # model-estimated probability [0, 1]
            'result_label': str,       # human-readable result
            'explanation': str,        # cautious language
            'feature_importance': dict # SHAP / importance values
        }
    """
    pipeline, model_name = load_best_model(disease)
    feature_names = load_feature_names(disease)

    # Build input DataFrame preserving feature order
    if feature_names:
        X_df = pd.DataFrame([{col: input_data.get(col, np.nan) for col in feature_names}])
    else:
        X_df = pd.DataFrame([input_data])

    # Prediction
    pred = int(pipeline.predict(X_df)[0])

    if hasattr(pipeline, "predict_proba"):
        prob = float(pipeline.predict_proba(X_df)[0][1])
    elif hasattr(pipeline, "decision_function"):
        score = pipeline.decision_function(X_df)[0]
        # Sigmoid to map to [0,1]
        prob = float(1 / (1 + np.exp(-score)))
    else:
        prob = float(pred)

    # Cautious, educational language (never claim definitive diagnosis)
    if pred == 1:
        result_label = "Higher model-estimated likelihood"
        explanation = (
            f"Based on the entered values, the {_friendly_name(model_name)} model estimates a "
            f"higher likelihood of {_disease_label(disease)} (model probability: {prob:.1%}). "
            "This is NOT a medical diagnosis. These results are for educational purposes only."
        )
    else:
        result_label = "Lower model-estimated likelihood"
        explanation = (
            f"Based on the entered values, the {_friendly_name(model_name)} model estimates a "
            f"lower likelihood of {_disease_label(disease)} (model probability: {prob:.1%}). "
            "This is NOT a medical diagnosis. These results are for educational purposes only."
        )

    # SHAP / feature importance
    feature_importance = _get_shap_values(pipeline, X_df, feature_names)

    return {
        "disease": disease,
        "model_name": _friendly_name(model_name),
        "prediction": pred,
        "probability": round(prob, 4),
        "result_label": result_label,
        "explanation": explanation,
        "feature_importance": feature_importance,
    }


def _friendly_name(model_key: str) -> str:
    mapping = {
        "logistic_regression": "Logistic Regression",
        "svm": "Support Vector Machine",
        "random_forest": "Random Forest",
        "xgboost": "XGBoost",
    }
    return mapping.get(model_key.lower(), model_key.replace("_", " ").title())


def _disease_label(disease: str) -> str:
    mapping = {
        "heart": "Heart Disease",
        "diabetes": "Diabetes",
        "breast_cancer": "Breast Cancer",
    }
    return mapping.get(disease, disease.replace("_", " ").title())
