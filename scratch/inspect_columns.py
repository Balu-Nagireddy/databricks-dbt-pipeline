"""Quick schema introspection for all serving tables."""
from src.warehouse.connection import connection_manager
from sqlalchemy import text

tables = [
    "serving.fact_sales_daily",
    "serving.fact_sales_monthly",
    "serving.dim_sales_revenue_by_state",
    "serving.dim_customers_clv",
    "serving.dim_customers_top_cities",
    "serving.fact_customers_repeat_stats",
    "serving.dim_products_performance",
    "serving.dim_products_category_performance",
    "serving.fact_payments_method_dist",
    "serving.fact_payments_installments",
    "serving.fact_logistics_delivery_by_state",
    "serving.fact_logistics_delivery_success_rates",
    "serving.fact_logistics_seller_shipping_perf",
    "serving.fact_executive_kpis",
]

conn = connection_manager.get_connection()
for t in tables:
    rows = conn.execute(text(f"SELECT * FROM {t} LIMIT 1;")).mappings().fetchone()
    cols = list(rows.keys()) if rows else "empty"
    print(f"{t}: {cols}")
conn.close()
