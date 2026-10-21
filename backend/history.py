"""
Prediction history endpoint.
GET /api/prediction-history
"""
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db, get_recent_predictions

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/prediction-history", tags=["History"])
async def get_prediction_history(limit: int = 20, db: Session = Depends(get_db)):
    """Return recent anonymised prediction history."""
    if limit < 1 or limit > 100:
        limit = 20
    records = get_recent_predictions(db, limit=limit)
    history = [
        {
            "id": r.id,
            "disease_type": r.disease_type,
            "model_name": r.model_name,
            "prediction_result": r.prediction_result,
            "estimated_probability": r.estimated_probability,
            "result_label": r.result_label,
            "timestamp": r.timestamp.isoformat(),
        }
        for r in records
    ]
    return {"history": history, "count": len(history)}
