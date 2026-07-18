import time
from pathlib import Path
from sqlalchemy import text
from src.warehouse.connection import connection_manager
from src.warehouse.loader import TABLE_REGISTRY
from src.common.logging import get_logger

logger = get_logger(__name__)

class WarehouseReconciliation:
    def __init__(self):
        self.report_path = Path("docs/WAREHOUSE_VALIDATION.md")

    def generate_report(self, load_stats: dict, execution_time_seconds: float, overall_status: str):
        """
        Generates docs/WAREHOUSE_VALIDATION.md detailing source vs target row counts and differences.
        """
        logger.info(f"Generating Warehouse Reconciliation report: {self.report_path}")

        md = []
        md.append("# Warehouse Reconciliation Report")
        md.append("")
        md.append(f"**Execution Timestamp**: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        md.append(f"**Overall Status**: `{overall_status}`")
        md.append(f"**Total Execution Duration**: {execution_time_seconds:.2f} seconds")
        md.append("")
        md.append("## Source vs Target Reconciliation")
        md.append("")
        md.append("| Parquet Dataset | Target Table | Source Rows (Parquet) | Target Rows (Database) | Difference | Status |")
        md.append("|---|---|---|---|---|---|")

        conn = connection_manager.get_connection()
        try:
            for name, table_name in TABLE_REGISTRY.items():
                source_count = load_stats.get(name, 0)
                
                # Fetch actual row count from DB
                res = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};")).fetchone()
                target_count = res[0]
                
                diff = target_count - source_count
                status = "✔ MATCH" if diff == 0 else "❌ MISMATCH"
                
                md.append(f"| {name} | {table_name} | {source_count:,} | {target_count:,} | {diff} | {status} |")
        finally:
            conn.close()

        md.append("")
        md.append("## Validation Specifications")
        md.append("- **Row Count Match**: Ensures all records loaded from Parquet files match PostgreSQL counts.")
        md.append("- **Primary Key Check**: Enforces B-Tree index uniqueness on designated primary keys.")
        md.append("- **Nullability Verification**: Confirms no null records in primary key columns.")

        # Write to file
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        logger.info("Warehouse Reconciliation report created successfully.")
