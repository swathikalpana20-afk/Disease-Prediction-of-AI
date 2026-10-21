"""
FastAPI application entry point.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.database import create_tables
from api.health import router as health_router
from api.models import router as models_router
from api.prediction import router as prediction_router
from api.history import router as history_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create DB tables."""
    logger.info("Starting Disease Prediction API...")
    create_tables()
    logger.info("Database tables ready.")
    yield
    logger.info("Shutting down Disease Prediction API.")


app = FastAPI(
    title="Disease Prediction API",
    description=(
        "Educational ML API for Heart Disease, Diabetes, and Breast Cancer prediction. "
        "**NOT for medical diagnosis.** All predictions are model estimates for educational purposes only."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS — allow React dev server and production build
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Global exception handler — never expose stack traces to frontend
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again."},
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health_router, prefix="/api")
app.include_router(models_router, prefix="/api")
app.include_router(prediction_router, prefix="/api")
app.include_router(history_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Disease Prediction API",
        "docs": "/docs",
        "disclaimer": (
            "Educational purpose only. Not a medical diagnosis. "
            "Consult a qualified healthcare professional."
        ),
    }
