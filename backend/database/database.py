"""
SQLite database setup using SQLAlchemy (async).
Stores anonymised prediction history — no personally identifying patient data.
"""
import os
from datetime import datetime
from pathlib import Path
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, create_engine, text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "predictions.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PredictionHistory(Base):
    """
    Stores anonymised prediction events.
    Does NOT store input feature values or any personally identifiable information.
    """
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    disease_type = Column(String(50), nullable=False)       # 'heart', 'diabetes', 'breast_cancer'
    model_name = Column(String(100), nullable=False)        # e.g. 'Random Forest'
    prediction_result = Column(Integer, nullable=False)      # 0 or 1
    estimated_probability = Column(Float, nullable=False)    # model-estimated probability
    result_label = Column(String(200), nullable=False)       # human-readable label
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency: yield a DB session, close on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_prediction(db, result: dict):
    """Persist an anonymised prediction record."""
    record = PredictionHistory(
        disease_type=result["disease"],
        model_name=result["model_name"],
        prediction_result=result["prediction"],
        estimated_probability=result["probability"],
        result_label=result["result_label"],
        timestamp=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_recent_predictions(db, limit: int = 20) -> list:
    return (
        db.query(PredictionHistory)
        .order_by(PredictionHistory.timestamp.desc())
        .limit(limit)
        .all()
    )
