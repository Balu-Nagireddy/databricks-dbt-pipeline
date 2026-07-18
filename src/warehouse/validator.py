from sqlalchemy import text
from src.warehouse.connection import connection_manager
from src.common.logging import get_logger

logger = get_logger(__name__)

# Primary keys map for duplicate verification
PRIMARY_KEYS = {
    "serving.fact_sales_daily": "sale_date",
    "serving.fact_sales_weekly": "sale_week",
    "serving.fact_sales_monthly": "sale_month",
    "serving.fact_sales_yearly": "sale_year",
    "serving.dim_sales_revenue_by_state": "customer_state",
    "serving.dim_sales_revenue_by_city": "customer_city, customer_state",
    "serving.dim_sales_revenue_by_seller": "seller_id",
    "serving.dim_sales_revenue_by_category": "product_category_name_english",
    "serving.dim_sales_top_selling_products": "product_id",
    "serving.fact_sales_average_order_value": None,
    "serving.dim_customers_clv": "customer_unique_id",
    "serving.dim_customers_top_cities": "customer_city, customer_state",
    "serving.fact_customers_repeat_stats": "is_repeat_customer",
    "serving.dim_products_performance": "product_id",
    "serving.dim_products_category_performance": "product_category_name_english",
    "serving.fact_payments_method_dist": "payment_type",
    "serving.fact_payments_installments": "payment_installments",
    "serving.fact_logistics_delivery_by_state": "customer_state",
    "serving.fact_logistics_delivery_success_rates": None,
    "serving.fact_logistics_seller_shipping_perf": "seller_id",
    "serving.fact_executive_kpis": None
}

class WarehouseValidator:
    def __init__(self):
        self.conn_manager = connection_manager

    def validate_table(self, table_name: str, expected_row_count: int) -> bool:
        """
        Runs quality validation checks on a serving table:
        - Row Count Verification
        - Duplicate Primary Key Check
        - Nullability compliance
        """
        logger.info(f"Starting quality validations on table: {table_name}")
        conn = self.conn_manager.get_connection()
        try:
            # 1. Row Count Validation
            res = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};")).fetchone()
            actual_count = res[0]
            logger.info(f"Row count validation -> Expected: {expected_row_count}, Actual: {actual_count}")
            if actual_count != expected_row_count:
                logger.error(f"Row count validation FAILED for {table_name}. Count mismatch!")
                return False

            # 2. Duplicate Primary Key Check
            pk = PRIMARY_KEYS.get(table_name)
            if pk:
                dup_query = f"SELECT {pk}, COUNT(*) FROM {table_name} GROUP BY {pk} HAVING COUNT(*) > 1;"
                dup_res = conn.execute(text(dup_query)).fetchall()
                if dup_res:
                    logger.error(f"Duplicate primary key validation FAILED for {table_name}! Duplicates found: {dup_res}")
                    return False
                logger.info(f"Primary key uniqueness validation PASSED for {table_name}.")

            # 3. Nullability Check on Primary Key
            if pk:
                pk_cols = [c.strip() for c in pk.split(",")]
                null_conditions = " OR ".join([f"{col} IS NULL" for col in pk_cols])
                null_query = f"SELECT COUNT(*) FROM {table_name} WHERE {null_conditions};"
                null_res = conn.execute(text(null_query)).fetchone()[0]
                if null_res > 0:
                    logger.error(f"Null primary key validation FAILED for {table_name}. Found {null_res} null PKs.")
                    return False
                logger.info(f"Null primary key check PASSED for {table_name}.")

            logger.info(f"All validations PASSED for {table_name}.")
            return True
        finally:
            conn.close()

    def run_all_validations(self, stats: dict) -> bool:
        """
        Validates all tables loaded in registry.
        """
        from src.warehouse.loader import TABLE_REGISTRY
        success = True
        for name, table_name in TABLE_REGISTRY.items():
            expected = stats.get(name, 0)
            if not self.validate_table(table_name, expected):
                success = False
        return success
