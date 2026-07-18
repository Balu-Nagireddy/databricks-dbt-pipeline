"""
Health & version endpoints.
"""
import os
from datetime import datetime, timezone
from fastapi import APIRouter
from src.backend.database import ping_db
from src.backend.schemas import HealthResponse, VersionResponse
from src.backend.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
    summary="API health check",
    description="Returns the current API status and database connectivity.",
)
def health_check():
    db_ok = ping_db()
    return HealthResponse(
        status="ok" if db_ok else "degraded",
        database="connected" if db_ok else "unreachable",
        version=settings.VERSION,
        timestamp=datetime.now(timezone.utc),
    )


@router.get(
    "/version",
    response_model=VersionResponse,
    summary="API version metadata",
)
def version():
    return VersionResponse(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=os.getenv("APP_ENV", "development"),
    )
