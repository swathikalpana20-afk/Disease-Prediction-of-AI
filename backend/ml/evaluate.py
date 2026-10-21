"""
Model evaluation: computes Accuracy, Precision, Recall, F1, ROC-AUC,
and Confusion Matrix for each model. Saves results as JSON.
"""
import numpy as np
import logging
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

logger = logging.getLogger(__name__)


def evaluate_model(pipeline, X_test, y_test, model_name: str) -> dict:
    """
    Evaluate a fitted pipeline on the test set.
    Returns a dict of metrics.

    Note on metric choice for medical screening:
    Recall (Sensitivity) is particularly important in medical screening contexts
    because a false negative (missing a real case) is typically more harmful than
    a false positive. We report all metrics and select the best model based on
    a balanced F1 score rather than accuracy alone.
    """
    y_pred = pipeline.predict(X_test)
    y_prob = None

    if hasattr(pipeline, "predict_proba"):
        y_prob = pipeline.predict_proba(X_test)[:, 1]
    elif hasattr(pipeline, "decision_function"):
        scores = pipeline.decision_function(X_test)
        # Normalise to [0, 1] range for SVM
        y_prob = (scores - scores.min()) / (scores.max() - scores.min() + 1e-9)

    cm = confusion_matrix(y_test, y_pred).tolist()

    metrics = {
        "model": model_name,
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_prob)) if y_prob is not None else 0.0, 4),
        "confusion_matrix": cm,
    }

    # Build ROC curve data points
    if y_prob is not None:
        from sklearn.metrics import roc_curve
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        # Downsample to ~50 points for JSON storage
        idx = np.linspace(0, len(fpr) - 1, min(50, len(fpr)), dtype=int)
        metrics["roc_curve"] = {
            "fpr": [round(float(x), 4) for x in fpr[idx]],
            "tpr": [round(float(x), 4) for x in tpr[idx]],
        }

    logger.info(
        f"[{model_name}] Acc={metrics['accuracy']:.3f} "
        f"P={metrics['precision']:.3f} R={metrics['recall']:.3f} "
        f"F1={metrics['f1_score']:.3f} AUC={metrics['roc_auc']:.3f}"
    )
    return metrics


def select_best_model(all_metrics: list) -> str:
    """
    Select the best model by F1 score (balanced metric for imbalanced medical data).
    Returns the model name string.

    Medical note: We prioritise F1 over accuracy because medical datasets can be
    imbalanced, and accuracy alone can be misleading (a model that always predicts
    the majority class gets high accuracy but zero recall).
    """
    best = max(all_metrics, key=lambda m: m["f1_score"])
    logger.info(f"Best model selected: {best['model']} (F1={best['f1_score']:.3f})")
    return best["model"]


def build_metrics_summary(disease: str, dataset_info: dict, all_metrics: list, best_model_name: str) -> dict:
    """Assemble complete metrics JSON to save to disk."""
    return {
        "disease": disease,
        "dataset": dataset_info,
        "best_model": best_model_name,
        "selection_criterion": "F1 Score (balances precision and recall; preferred over accuracy for medical screening tasks)",
        "models": all_metrics,
    }
