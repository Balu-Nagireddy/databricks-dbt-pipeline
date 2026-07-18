"""
SQLAlchemy 2.x database engine and session configuration.
Provides a thread-safe, pooled database session factory.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from src.backend.config import settings
from src.common.logging import get_logger

logger = get_logger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Session:
    """
    Dependency that yields a database session per request and
    ensures the session is closed upon completion or error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ping_db() -> bool:
    """Health check — verifies database reachability."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error(f"Database ping failed: {exc}")
        return False
