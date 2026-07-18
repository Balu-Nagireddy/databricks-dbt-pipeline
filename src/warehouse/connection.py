import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from src.config import settings
from src.common.logging import get_logger

logger = get_logger(__name__)

# Connection retry settings
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5

class WarehouseConnectionManager:
    def __init__(self):
        self.db_url = settings.database_url
        if not self.db_url:
            raise ValueError("DATABASE_URL setting is not configured.")
        
        # Initialize connection pool using SQLAlchemy
        logger.info("Initializing SQLAlchemy PostgreSQL Connection Pool...")
        self.engine = create_engine(
            self.db_url,
            pool_size=10,
            max_overflow=5,
            pool_recycle=1800, # Recycle connections after 30 minutes
            pool_pre_ping=True  # Confirm connection validity before executing queries
        )

    def get_connection(self):
        """
        Acquire a raw connection from the pool with retry logic for resiliency.
        """
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Acquire connection (pre-ping handles verification)
                conn = self.engine.connect()
                return conn
            except OperationalError as e:
                logger.warning(
                    f"OperationalError during connection attempt {attempt}/{MAX_RETRIES}: {e}. "
                    f"Retrying in {RETRY_DELAY_SECONDS} seconds..."
                )
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_SECONDS)
                else:
                    logger.error("Failed to connect to the warehouse database after maximum retry attempts.")
                    raise e

    def shutdown(self):
        """
        Gracefully close all pooled connections.
        """
        logger.info("Disposing connection pool and shutting down engine...")
        self.engine.dispose()

# Global connection manager instance
connection_manager = WarehouseConnectionManager()
