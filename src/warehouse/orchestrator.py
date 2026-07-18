import time
from pathlib import Path
from src.warehouse.connection import connection_manager
from src.warehouse.ddl import execute_ddl
from src.warehouse.loader import WarehouseLoader
from src.warehouse.validator import WarehouseValidator
from src.warehouse.reconciliation import WarehouseReconciliation
from src.common.logging import get_logger

logger = get_logger(__name__)

class WarehouseOrchestrator:
    def __init__(self):
        self.loader = WarehouseLoader()
        self.validator = WarehouseValidator()
        self.reconciler = WarehouseReconciliation()

    def run_pipeline(self):
        start_time = time.time()
        logger.info("Starting Warehouse Ingestion Pipeline...")
        
        load_stats = {}
        overall_status = "SUCCESS"
        
        try:
            # 1. Establish initial connection and execute DDL schemas
            ddl_path = Path("docs/schema_init.sql")
            logger.info("Initializing serving DDL schemas and indexes...")
            execute_ddl(ddl_path)

            # 2. Ingest Gold Marts
            logger.info("Starting Gold analytical marts load...")
            load_stats = self.loader.load_all_marts()
            logger.info("All Gold analytical marts successfully loaded.")

            # 3. Validate Data Quality
            logger.info("Starting post-load database validations...")
            validations_passed = self.validator.run_all_validations(load_stats)
            if not validations_passed:
                overall_status = "FAILED"
                logger.error("Warehouse data quality validations FAILED.")
                raise ValueError("Database table validations failed. Aborting pipeline.")
            logger.info("All data quality validations passed successfully.")

        except Exception as e:
            overall_status = "FAILED"
            logger.error(f"Warehouse Orchestrator pipeline failed: {e}")
            raise e
        finally:
            # 4. Generate Reconciliation Report and disconnect
            elapsed = time.time() - start_time
            self.reconciler.generate_report(load_stats, elapsed, overall_status)
            connection_manager.shutdown()
            logger.info(f"Warehouse Ingestion completed with status: {overall_status} in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    orchestrator = WarehouseOrchestrator()
    orchestrator.run_pipeline()
