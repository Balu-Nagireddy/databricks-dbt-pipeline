import pandas as pd
from pathlib import Path
from sqlalchemy import text
from src.config import settings
from src.warehouse.transaction import db_transaction
from src.common.logging import get_logger

logger = get_logger(__name__)

# Registry mapping Gold Parquet folder name to PostgreSQL serving schema table name
TABLE_REGISTRY = {
    "daily_sales": "serving.fact_sales_daily",
    "weekly_sales": "serving.fact_sales_weekly",
    "monthly_sales": "serving.fact_sales_monthly",
    "yearly_sales": "serving.fact_sales_yearly",
    "revenue_by_state": "serving.dim_sales_revenue_by_state",
    "revenue_by_city": "serving.dim_sales_revenue_by_city",
    "revenue_by_seller": "serving.dim_sales_revenue_by_seller",
    "revenue_by_category": "serving.dim_sales_revenue_by_category",
    "top_selling_products": "serving.dim_sales_top_selling_products",
    "average_order_value": "serving.fact_sales_average_order_value",
    "customer_lifetime_value": "serving.dim_customers_clv",
    "top_customer_cities": "serving.dim_customers_top_cities",
    "repeat_customer_stats": "serving.fact_customers_repeat_stats",
    "product_performance": "serving.dim_products_performance",
    "category_performance": "serving.dim_products_category_performance",
    "payment_method_distribution": "serving.fact_payments_method_dist",
    "payment_installments_analysis": "serving.fact_payments_installments",
    "delivery_by_state": "serving.fact_logistics_delivery_by_state",
    "delivery_success_rates": "serving.fact_logistics_delivery_success_rates",
    "seller_shipping_performance": "serving.fact_logistics_seller_shipping_perf",
    "executive_kpis": "serving.fact_executive_kpis"
}

def locate_gold_dataset(name: str) -> Path:
    """
    Search for a Gold Parquet directory under data/gold/ subfolders.
    """
    gold_dir = settings.gold_path
    subdirs = ["sales", "customers", "products", "finance", "logistics", "executive"]
    for subdir in subdirs:
        target_path = gold_dir / subdir / name
        if target_path.exists():
            return target_path
    raise FileNotFoundError(f"Gold Parquet dataset '{name}' could not be located in data/gold/ subdirs.")

class WarehouseLoader:
    def load_mart(self, name: str, table_name: str) -> int:
        """
        Loads a single Gold Parquet dataset into PostgreSQL serving schema.
        Uses a Full Refresh (Truncate and Load) pattern inside a transaction.
        """
        parquet_path = locate_gold_dataset(name)
        logger.info(f"Reading Gold dataset '{name}' from Parquet: {parquet_path}")

        # Read parquet into pandas
        df = pd.read_parquet(str(parquet_path))
        row_count = len(df)
        logger.info(f"Loaded {row_count} records from Parquet.")

        # Truncate and bulk-insert data inside a transaction
        with db_transaction() as conn:
            # 1. Truncate table
            logger.info(f"Truncating table {table_name} for idempotent full refresh...")
            conn.execute(text(f"TRUNCATE TABLE {table_name} CASCADE;"))

            # 2. Write to PostgreSQL using pandas to_sql
            logger.info(f"Writing {row_count} records to {table_name}...")
            # We strip schema prefix to pass schema parameter to to_sql
            schema_name, raw_table_name = table_name.split(".")
            df.to_sql(
                name=raw_table_name,
                con=conn,
                schema=schema_name,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=10000
            )

        logger.info(f"Successfully loaded '{name}' into {table_name}.")
        return row_count

    def load_all_marts(self) -> dict:
        """
        Iterates over the TABLE_REGISTRY and loads each dataset.
        Returns a dictionary of counts loaded per table.
        """
        stats = {}
        for name, table_name in TABLE_REGISTRY.items():
            try:
                rows_loaded = self.load_mart(name, table_name)
                stats[name] = rows_loaded
            except Exception as e:
                logger.error(f"Error loading mart '{name}' into {table_name}: {e}")
                raise e
        return stats
