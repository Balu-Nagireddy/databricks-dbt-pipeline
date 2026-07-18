# Index Strategy Document

This document defines the indexing strategy for the `serving` database schema on Supabase.

## 1. Indexing Design Principles

PostgreSQL is a read-heavy query-serving database layer for FastAPI read-only APIs and dbt. To guarantee sub-second responses:
1. **Implicit PK Indexes**: PostgreSQL automatically creates unique B-Tree indexes for all primary key constraints.
2. **FK Indexes**: B-Tree indexes will be created on columns that act as relations between datasets (e.g. `seller_id`, `product_id`).
3. **Low-Cardinality Exclusions**: Indexes will *not* be created on low-cardinality flags (e.g. `is_repeat_customer`), as B-Tree performance declines below 10-15% selectivity.
4. **Range Scan Indexing**: High-resolution dates (e.g. `sale_date`) are indexed to optimize temporal filters (`WHERE sale_date BETWEEN ...`).

## 2. Specific Serving Indexes

### Sales Domain Indexes

```sql
-- Temporal Range Scans for Sales dashboards
CREATE INDEX IF NOT EXISTS idx_sales_daily_date ON serving.fact_sales_daily(sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_weekly_date ON serving.fact_sales_weekly(sale_week);
CREATE INDEX IF NOT EXISTS idx_sales_monthly_date ON serving.fact_sales_monthly(sale_month);

-- Geo-analytics distribution scans
CREATE INDEX IF NOT EXISTS idx_sales_state_revenue ON serving.dim_sales_revenue_by_state(total_revenue DESC);
CREATE INDEX IF NOT EXISTS idx_sales_city_revenue ON serving.dim_sales_revenue_by_city(total_revenue DESC);

-- Category filtering for products
CREATE INDEX IF NOT EXISTS idx_sales_category_rev ON serving.dim_sales_revenue_by_category(total_revenue DESC);
```

### Customer Domain Indexes

```sql
-- Segmented searches for marketing campaigns
CREATE INDEX IF NOT EXISTS idx_customers_segment ON serving.dim_customers_clv(customer_segment);
CREATE INDEX IF NOT EXISTS idx_customers_clv_val ON serving.dim_customers_clv(lifetime_value DESC);
```

### Product Domain Indexes

```sql
-- Top products rankings
CREATE INDEX IF NOT EXISTS idx_products_perf_rev ON serving.dim_products_performance(total_revenue DESC);
CREATE INDEX IF NOT EXISTS idx_products_category ON serving.dim_products_performance(product_category_name_english);
```

### Logistics Domain Indexes

```sql
-- SLA tracking scans
CREATE INDEX IF NOT EXISTS idx_logistics_state_duration ON serving.fact_logistics_delivery_by_state(avg_delivery_duration_days DESC);
CREATE INDEX IF NOT EXISTS idx_logistics_seller_shipping ON serving.fact_logistics_seller_shipping_perf(avg_shipping_duration_days DESC);
```
