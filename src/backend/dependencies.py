"""
Shared FastAPI dependency injection helpers.
"""
from fastapi import Query
from src.backend.config import settings


def pagination_params(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(
        default=settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Records per page",
    ),
) -> dict:
    """Returns offset + limit dict for paginated SQL queries."""
    return {"offset": (page - 1) * limit, "limit": limit}
