from contextlib import contextmanager
from src.warehouse.connection import connection_manager
from src.common.logging import get_logger

logger = get_logger(__name__)

@contextmanager
def db_transaction():
    """
    Context manager to execute database queries inside a transaction.
    Automatically commits on success or rolls back on exception/error.
    """
    connection = connection_manager.get_connection()
    transaction = connection.begin()
    try:
        yield connection
        transaction.commit()
    except Exception as e:
        logger.error(f"Transaction failed. Rolling back changes. Error: {e}")
        transaction.rollback()
        raise e
    finally:
        connection.close()
