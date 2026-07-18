# Database Schema Design

This document details the PostgreSQL schema layout, naming conventions, and domain ownership.

## 1. Schema Layout

To isolate the Gold analytics tables from public Supabase tables and application schemas, all tables are placed inside a dedicated PostgreSQL schema:
- Schema Name: **`serving`**

```sql
CREATE SCHEMA IF NOT EXISTS serving;
```

## 2. Naming Conventions

To ensure uniform schema definitions:
- **Table Names**: All lowercase, using snake_case. Prefix indicates the model pattern:
  - `dim_`: Dimension tables containing descriptive attributes (e.g. `dim_customers_clv`).
  - `fact_`: Fact tables containing metric measurements and temporal aggregations (e.g. `fact_sales_daily`).
- **Columns**: Lowercase snake_case.
  - IDs: Suffix `_id` (e.g. `customer_unique_id`, `product_id`).
  - Dates: Suffix `_date` (e.g. `sale_date`).
  - Timestamps: Suffix `_timestamp` or `_at` (e.g. `_loaded_at`).
  - Monetary values: Suffix `_value`, `_price`, or `_revenue` (e.g. `total_revenue`).

## 3. Domain Ownership & Table Registry

Each business domain owns its respective serving tables:

| Domain | Table Name | Type | Description |
|---|---|---|---|
| **Sales** | `serving.fact_sales_daily` | Fact | Daily aggregated sales and orders |
| **Sales** | `serving.fact_sales_weekly` | Fact | Weekly aggregated sales and orders |
| **Sales** | `serving.fact_sales_monthly` | Fact | Monthly aggregated sales and orders |
| **Sales** | `serving.fact_sales_yearly` | Fact | Yearly aggregated sales and orders |
| **Sales** | `serving.dim_sales_revenue_by_state` | Dimension | Sales distribution by geographical state |
| **Sales** | `serving.dim_sales_revenue_by_city` | Dimension | Sales distribution by geographical city |
| **Sales** | `serving.dim_sales_revenue_by_seller` | Dimension | Revenue contribution per individual seller |
| **Sales** | `serving.dim_sales_revenue_by_category` | Dimension | Revenue contribution per product category |
| **Sales** | `serving.dim_sales_top_selling_products` | Dimension | Top products by units sold |
| **Sales** | `serving.fact_sales_average_order_value` | Fact | Overall Average Order Value (AOV) |
| **Customers** | `serving.dim_customers_clv` | Dimension | Customer Lifetime Value, segments, and order counts |
| **Customers** | `serving.dim_customers_top_cities` | Dimension | Leading customer geographic cities |
| **Customers** | `serving.fact_customers_repeat_stats` | Fact | Counts of single-time vs repeat buyers |
| **Products** | `serving.dim_products_performance` | Dimension | Individual product unit sales and total revenue |
| **Products** | `serving.dim_products_category_performance` | Dimension | Sales volume and revenues by product category |
| **Finance** | `serving.fact_payments_method_dist` | Fact | Aggregated payment methods usage stats |
| **Finance** | `serving.fact_payments_installments` | Fact | Average payment installments configuration impact |
| **Logistics** | `serving.fact_logistics_delivery_by_state` | Fact | Shipping transit times by destination state |
| **Logistics** | `serving.fact_logistics_delivery_success_rates` | Fact | Successful deliveries validation metrics |
| **Logistics** | `serving.fact_logistics_seller_shipping_perf` | Fact | Average shipping delay durations per seller |
| **Executive** | `serving.fact_executive_kpis` | Fact | Consolidated corporate high-level metrics |
