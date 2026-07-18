-- ============================================================================
-- SQL Ingestion & Serving Schema Initialisation Script
-- Schema: serving
-- Target Platform: PostgreSQL (Supabase)
-- ============================================================================

DROP SCHEMA IF EXISTS serving CASCADE;
CREATE SCHEMA serving;

-- ============================================================================
-- 1. SALES DOMAIN TABLES
-- ============================================================================

-- Daily Sales Fact
CREATE TABLE IF NOT EXISTS serving.fact_sales_daily (
    sale_date DATE PRIMARY KEY,
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_orders INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Weekly Sales Fact
CREATE TABLE IF NOT EXISTS serving.fact_sales_weekly (
    sale_week DATE PRIMARY KEY,
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_orders INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Monthly Sales Fact
CREATE TABLE IF NOT EXISTS serving.fact_sales_monthly (
    sale_month DATE PRIMARY KEY,
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_orders INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Yearly Sales Fact
CREATE TABLE IF NOT EXISTS serving.fact_sales_yearly (
    sale_year DATE PRIMARY KEY,
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_orders INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- State Revenue Dimension
CREATE TABLE IF NOT EXISTS serving.dim_sales_revenue_by_state (
    customer_state VARCHAR(5) PRIMARY KEY,
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_orders INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- City Revenue Dimension
CREATE TABLE IF NOT EXISTS serving.dim_sales_revenue_by_city (
    customer_city VARCHAR(100),
    customer_state VARCHAR(5),
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_orders INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (customer_city, customer_state)
);

-- Seller Revenue Dimension
CREATE TABLE IF NOT EXISTS serving.dim_sales_revenue_by_seller (
    seller_id VARCHAR(50) PRIMARY KEY,
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_orders INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Category Revenue Dimension
CREATE TABLE IF NOT EXISTS serving.dim_sales_revenue_by_category (
    product_category_name_english VARCHAR(100) PRIMARY KEY,
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_orders INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Top Selling Products Dimension
CREATE TABLE IF NOT EXISTS serving.dim_sales_top_selling_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name_english VARCHAR(100),
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_units_sold INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Average Order Value Fact (Single Record)
CREATE TABLE IF NOT EXISTS serving.fact_sales_average_order_value (
    average_order_value DECIMAL(12, 2) NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ============================================================================
-- 2. CUSTOMER DOMAIN TABLES
-- ============================================================================

-- Customer Lifetime Value Dimension
CREATE TABLE IF NOT EXISTS serving.dim_customers_clv (
    customer_unique_id VARCHAR(50) PRIMARY KEY,
    total_orders INT NOT NULL,
    lifetime_value DECIMAL(12, 2) NOT NULL,
    avg_order_spend DECIMAL(12, 2) NOT NULL,
    is_repeat_customer BOOLEAN NOT NULL,
    customer_segment VARCHAR(20) NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Top Customer Cities Dimension
CREATE TABLE IF NOT EXISTS serving.dim_customers_top_cities (
    customer_city VARCHAR(100),
    customer_state VARCHAR(5),
    customer_count INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (customer_city, customer_state)
);

-- Customer Repeat Stats Fact
CREATE TABLE IF NOT EXISTS serving.fact_customers_repeat_stats (
    is_repeat_customer BOOLEAN PRIMARY KEY,
    customer_count INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ============================================================================
-- 3. PRODUCT DOMAIN TABLES
-- ============================================================================

-- Product Performance Dimension
CREATE TABLE IF NOT EXISTS serving.dim_products_performance (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name_english VARCHAR(100),
    units_sold INT NOT NULL,
    total_revenue DECIMAL(12, 2) NOT NULL,
    avg_unit_price DECIMAL(12, 2) NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Category Performance Dimension
CREATE TABLE IF NOT EXISTS serving.dim_products_category_performance (
    product_category_name_english VARCHAR(100) PRIMARY KEY,
    units_sold INT NOT NULL,
    total_revenue DECIMAL(12, 2) NOT NULL,
    avg_unit_price DECIMAL(12, 2) NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ============================================================================
-- 4. FINANCE DOMAIN TABLES
-- ============================================================================

-- Payment Method Distribution Fact
CREATE TABLE IF NOT EXISTS serving.fact_payments_method_dist (
    payment_type VARCHAR(30) PRIMARY KEY,
    transaction_count INT NOT NULL,
    total_payment_value DECIMAL(12, 2) NOT NULL,
    avg_transaction_value DECIMAL(12, 2) NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Payment Installments Analysis Fact
CREATE TABLE IF NOT EXISTS serving.fact_payments_installments (
    payment_installments INT PRIMARY KEY,
    transaction_count INT NOT NULL,
    total_payment_value DECIMAL(12, 2) NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ============================================================================
-- 5. LOGISTICS DOMAIN TABLES
-- ============================================================================

-- Delivery Duration by State Fact
CREATE TABLE IF NOT EXISTS serving.fact_logistics_delivery_by_state (
    customer_state VARCHAR(5) PRIMARY KEY,
    avg_delivery_duration_days DECIMAL(8, 2) NOT NULL,
    total_orders INT NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Delivery Success Rates Fact (Single Record)
CREATE TABLE IF NOT EXISTS serving.fact_logistics_delivery_success_rates (
    total_orders INT NOT NULL,
    total_delivered INT NOT NULL,
    total_late_orders INT NOT NULL,
    success_rate_percent DECIMAL(5, 2) NOT NULL,
    late_rate_percent DECIMAL(5, 2) NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Seller Shipping Performance Fact
CREATE TABLE IF NOT EXISTS serving.fact_logistics_seller_shipping_perf (
    seller_id VARCHAR(50) PRIMARY KEY,
    items_shipped INT NOT NULL,
    avg_shipping_duration_days DECIMAL(8, 2),
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ============================================================================
-- 6. EXECUTIVE DOMAIN TABLES
-- ============================================================================

-- Executive KPIs Fact (Single Record)
CREATE TABLE IF NOT EXISTS serving.fact_executive_kpis (
    total_revenue DECIMAL(12, 2) NOT NULL,
    total_orders INT NOT NULL,
    total_customers INT NOT NULL,
    total_products INT NOT NULL,
    total_sellers INT NOT NULL,
    average_delivery_time_days DECIMAL(8, 2) NOT NULL,
    average_review_score DECIMAL(4, 2) NOT NULL,
    _loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- ============================================================================
-- INDEXES DEFINITIONS
-- ============================================================================

-- Temporal range scan indices
CREATE INDEX IF NOT EXISTS idx_sales_daily_date ON serving.fact_sales_daily(sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_weekly_date ON serving.fact_sales_weekly(sale_week);
CREATE INDEX IF NOT EXISTS idx_sales_monthly_date ON serving.fact_sales_monthly(sale_month);

-- Revenue ranking performance indices
CREATE INDEX IF NOT EXISTS idx_sales_state_rev ON serving.dim_sales_revenue_by_state(total_revenue DESC);
CREATE INDEX IF NOT EXISTS idx_sales_city_rev ON serving.dim_sales_revenue_by_city(total_revenue DESC);
CREATE INDEX IF NOT EXISTS idx_sales_category_rev ON serving.dim_sales_revenue_by_category(total_revenue DESC);

-- Segmentation search index
CREATE INDEX IF NOT EXISTS idx_customers_segment ON serving.dim_customers_clv(customer_segment);
CREATE INDEX IF NOT EXISTS idx_customers_clv_val ON serving.dim_customers_clv(lifetime_value DESC);

-- Product category search indexes
CREATE INDEX IF NOT EXISTS idx_products_category ON serving.dim_products_performance(product_category_name_english);
CREATE INDEX IF NOT EXISTS idx_products_revenue ON serving.dim_products_performance(total_revenue DESC);

-- SLA tracking performance indices
CREATE INDEX IF NOT EXISTS idx_logistics_state_transit ON serving.fact_logistics_delivery_by_state(avg_delivery_duration_days DESC);
CREATE INDEX IF NOT EXISTS idx_logistics_seller_shipping ON serving.fact_logistics_seller_shipping_perf(avg_shipping_duration_days DESC);
