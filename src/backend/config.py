"""
Centralized API configuration.
Extends platform-level settings with API-specific concerns.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class APISettings:
    """API-specific configuration, driven entirely from environment variables."""

    # API metadata
    PROJECT_NAME: str = "Prism Analytics API"
    PROJECT_DESCRIPTION: str = (
        "A read-only analytics service exposing curated business metrics "
        "derived from the Spark/dbt data pipeline serving layer."
    )
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Runtime
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    HOST: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("FASTAPI_PORT", "8000"))

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 5
    DB_POOL_RECYCLE: int = 1800  # 30 minutes

    # CORS — allow all origins in dev; restrict in production
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173,http://localhost:8080"
        ).split(",")
        if origin.strip()
    ]

    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 500


settings = APISettings()
