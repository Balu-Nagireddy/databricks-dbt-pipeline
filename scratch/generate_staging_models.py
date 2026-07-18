import os
from pathlib import Path

tables = [
    ("fact_sales_daily", "fct_sales_daily"),
    ("fact_sales_weekly", "fct_sales_weekly"),
    ("fact_sales_monthly", "fct_sales_monthly"),
    ("fact_sales_yearly", "fct_sales_yearly"),
    ("dim_sales_revenue_by_state", "dim_sales_revenue_by_state"),
    ("dim_sales_revenue_by_city", "dim_sales_revenue_by_city"),
    ("dim_sales_revenue_by_seller", "dim_sales_revenue_by_seller"),
    ("dim_sales_revenue_by_category", "dim_sales_revenue_by_category"),
    ("dim_sales_top_selling_products", "dim_sales_top_selling_products"),
    ("fact_sales_average_order_value", "fct_sales_average_order_value"),
    ("dim_customers_clv", "dim_customers_clv"),
    ("dim_customers_top_cities", "dim_customers_top_cities"),
    ("fact_customers_repeat_stats", "fct_customers_repeat_stats"),
    ("dim_products_performance", "dim_products_performance"),
    ("dim_products_category_performance", "dim_products_category_performance"),
    ("fact_payments_method_dist", "fct_payments_method_dist"),
    ("fact_payments_installments", "fct_payments_installments"),
    ("fact_logistics_delivery_by_state", "fct_logistics_delivery_by_state"),
    ("fact_logistics_delivery_success_rates", "fct_logistics_delivery_success_rates"),
    ("fact_logistics_seller_shipping_perf", "fct_logistics_seller_shipping_perf"),
    ("fact_executive_kpis", "fct_executive_kpis")
]

def main():
    staging_dir = Path("analytics/models/staging")
    marts_dir = Path("analytics/models/marts")
    
    staging_dir.mkdir(parents=True, exist_ok=True)
    marts_dir.mkdir(parents=True, exist_ok=True)
    
    for db_name, model_name in tables:
        stg_name = f"stg_{db_name}"
        
        # Write staging model
        stg_path = staging_dir / f"{stg_name}.sql"
        stg_content = f"select * from {{{{ source('serving', '{db_name}') }}}}\n"
        stg_path.write_text(stg_content, encoding="utf-8")
        print(f"Created staging model: {stg_path}")
        
        # Write mart model
        mart_path = marts_dir / f"{model_name}.sql"
        mart_content = f"select * from {{{{ ref('{stg_name}') }}}}\n"
        mart_path.write_text(mart_content, encoding="utf-8")
        print(f"Created mart model: {mart_path}")

if __name__ == "__main__":
    main()
