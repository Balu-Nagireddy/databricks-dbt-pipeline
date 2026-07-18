"""
FastAPI Analytics API — main application entrypoint.

Registers all routers, configures CORS, exception handling,
timing middleware, OpenAPI documentation, and Prometheus metrics.
"""
import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

try:
    from prometheus_fastapi_instrumentator import Instrumentator
    PROMETHEUS_ENABLED = True
except ImportError:
    PROMETHEUS_ENABLED = False

from src.backend.config import settings
from src.backend.middleware import TimingMiddleware
from src.backend.routers import health, executive, sales, customers, products, finance, logistics
from src.common.logging import get_logger

logger = get_logger(__name__)


# ──────────────────────────────────────────────────────────────
# Lifespan — startup / shutdown hooks
# ──────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"[STARTUP] {settings.PROJECT_NAME} v{settings.VERSION} starting...")
    yield
    logger.info("[SHUTDOWN] Shutting down API server.")


# ──────────────────────────────────────────────────────────────
# Application factory
# ──────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── Timing + logging ──────────────────────────────────────────
app.add_middleware(TimingMiddleware)


# ── Global exception handlers ─────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


# ── Register routers ──────────────────────────────────────────
PREFIX = settings.API_V1_STR

app.include_router(health.router, prefix=PREFIX)
app.include_router(executive.router, prefix=PREFIX)
app.include_router(sales.router, prefix=PREFIX)
app.include_router(customers.router, prefix=PREFIX)
app.include_router(products.router, prefix=PREFIX)
app.include_router(finance.router, prefix=PREFIX)
app.include_router(logistics.router, prefix=PREFIX)

# ── Prometheus metrics (/metrics) ─────────────────────────────
if PROMETHEUS_ENABLED:
    Instrumentator(
        should_group_status_codes=True,
        excluded_handlers=["/metrics", "/"],
    ).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)


# ── Root redirect ─────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.backend.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
