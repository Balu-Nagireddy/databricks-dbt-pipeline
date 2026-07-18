# Warehouse Reconciliation Report

**Execution Timestamp**: 2026-07-18 15:09:59
**Overall Status**: `SUCCESS`
**Total Execution Duration**: 25.68 seconds

## Source vs Target Reconciliation

| Parquet Dataset | Target Table | Source Rows (Parquet) | Target Rows (Database) | Difference | Status |
|---|---|---|---|---|---|
| daily_sales | serving.fact_sales_daily | 616 | 616 | 0 | ✔ MATCH |
| weekly_sales | serving.fact_sales_weekly | 95 | 95 | 0 | ✔ MATCH |
| monthly_sales | serving.fact_sales_monthly | 24 | 24 | 0 | ✔ MATCH |
| yearly_sales | serving.fact_sales_yearly | 3 | 3 | 0 | ✔ MATCH |
| revenue_by_state | serving.dim_sales_revenue_by_state | 27 | 27 | 0 | ✔ MATCH |
| revenue_by_city | serving.dim_sales_revenue_by_city | 4,300 | 4,300 | 0 | ✔ MATCH |
| revenue_by_seller | serving.dim_sales_revenue_by_seller | 3,095 | 3,095 | 0 | ✔ MATCH |
| revenue_by_category | serving.dim_sales_revenue_by_category | 74 | 74 | 0 | ✔ MATCH |
| top_selling_products | serving.dim_sales_top_selling_products | 32,951 | 32,951 | 0 | ✔ MATCH |
| average_order_value | serving.fact_sales_average_order_value | 1 | 1 | 0 | ✔ MATCH |
| customer_lifetime_value | serving.dim_customers_clv | 95,420 | 95,420 | 0 | ✔ MATCH |
| top_customer_cities | serving.dim_customers_top_cities | 4,310 | 4,310 | 0 | ✔ MATCH |
| repeat_customer_stats | serving.fact_customers_repeat_stats | 2 | 2 | 0 | ✔ MATCH |
| product_performance | serving.dim_products_performance | 32,951 | 32,951 | 0 | ✔ MATCH |
| category_performance | serving.dim_products_category_performance | 74 | 74 | 0 | ✔ MATCH |
| payment_method_distribution | serving.fact_payments_method_dist | 5 | 5 | 0 | ✔ MATCH |
| payment_installments_analysis | serving.fact_payments_installments | 24 | 24 | 0 | ✔ MATCH |
| delivery_by_state | serving.fact_logistics_delivery_by_state | 27 | 27 | 0 | ✔ MATCH |
| delivery_success_rates | serving.fact_logistics_delivery_success_rates | 1 | 1 | 0 | ✔ MATCH |
| seller_shipping_performance | serving.fact_logistics_seller_shipping_perf | 3,095 | 3,095 | 0 | ✔ MATCH |
| executive_kpis | serving.fact_executive_kpis | 1 | 1 | 0 | ✔ MATCH |

## Validation Specifications
- **Row Count Match**: Ensures all records loaded from Parquet files match PostgreSQL counts.
- **Primary Key Check**: Enforces B-Tree index uniqueness on designated primary keys.
- **Nullability Verification**: Confirms no null records in primary key columns.