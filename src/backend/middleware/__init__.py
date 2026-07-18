"""
Timing and request-logging middleware.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.common.logging import get_logger

logger = get_logger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """Adds X-Process-Time header and logs every request/response."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"
        logger.info(
            f"{request.method} {request.url.path} "
            f"-> {response.status_code} ({duration_ms:.2f}ms)"
        )
        return response
