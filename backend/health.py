"""
Health check endpoint.
GET /api/health
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """Returns API health status."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Disease Prediction API",
        "version": "1.0.0",
    }
