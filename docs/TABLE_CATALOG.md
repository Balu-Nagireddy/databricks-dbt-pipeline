# Table Catalog

This catalog outlines all tables implemented inside the `serving` schema.

## 1. Schema Constraints
- **Primary Keys**: Explicitly defined on all tables to enforce record uniqueness in the serving layer.
- **Nullability**: Columns containing critical metrics (e.g. `total_revenue`, `lifetime_value`) are configured with `NOT NULL` constraints.
- **Audit Columns**: Each table has an ingestion audit column `_loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL`.

---

## 2. Table Specifications

### Sales Mart Tables

#### `serving.fact_sales_daily`
- **Primary Key**: `sale_date` (DATE)
- **Columns**:
  - `sale_date` DATE PRIMARY KEY
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `total_orders` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.fact_sales_weekly`
- **Primary Key**: `sale_week` (DATE)
- **Columns**:
  - `sale_week` DATE PRIMARY KEY
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `total_orders` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.fact_sales_monthly`
- **Primary Key**: `sale_month` (DATE)
- **Columns**:
  - `sale_month` DATE PRIMARY KEY
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `total_orders` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.fact_sales_yearly`
- **Primary Key**: `sale_year` (DATE)
- **Columns**:
  - `sale_year` DATE PRIMARY KEY
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `total_orders` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.dim_sales_revenue_by_state`
- **Primary Key**: `customer_state` (VARCHAR(5))
- **Columns**:
  - `customer_state` VARCHAR(5) PRIMARY KEY
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `order_count` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.dim_sales_revenue_by_city`
- **Primary Key**: `customer_city` (VARCHAR(100))
- **Columns**:
  - `customer_city` VARCHAR(100) PRIMARY KEY
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `order_count` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.dim_sales_revenue_by_seller`
- **Primary Key**: `seller_id` (VARCHAR(50))
- **Columns**:
  - `seller_id` VARCHAR(50) PRIMARY KEY
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `order_count` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.dim_sales_revenue_by_category`
- **Primary Key**: `product_category_name_english` (VARCHAR(100))
- **Columns**:
  - `product_category_name_english` VARCHAR(100) PRIMARY KEY
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `order_count` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.dim_sales_top_selling_products`
- **Primary Key**: `product_id` (VARCHAR(50))
- **Columns**:
  - `product_id` VARCHAR(50) PRIMARY KEY
  - `units_sold` INT NOT NULL
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.fact_sales_average_order_value`
- **Primary Key**: None (single row lookup)
- **Columns**:
  - `average_order_value` DECIMAL(12, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

---

### Customer Mart Tables

#### `serving.dim_customers_clv`
- **Primary Key**: `customer_unique_id` (VARCHAR(50))
- **Columns**:
  - `customer_unique_id` VARCHAR(50) PRIMARY KEY
  - `total_orders` INT NOT NULL
  - `lifetime_value` DECIMAL(12, 2) NOT NULL
  - `avg_order_spend` DECIMAL(12, 2) NOT NULL
  - `is_repeat_customer` BOOLEAN NOT NULL
  - `customer_segment` VARCHAR(20) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.dim_customers_top_cities`
- **Primary Key**: `customer_city` (VARCHAR(100))
- **Columns**:
  - `customer_city` VARCHAR(100) PRIMARY KEY
  - `customer_count` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.fact_customers_repeat_stats`
- **Primary Key**: `is_repeat_customer` (BOOLEAN)
- **Columns**:
  - `is_repeat_customer` BOOLEAN PRIMARY KEY
  - `customer_count` INT NOT NULL
  - `_loaded_at` TIMESTAMPTZ

---

### Product Mart Tables

#### `serving.dim_products_performance`
- **Primary Key**: `product_id` (VARCHAR(50))
- **Columns**:
  - `product_id` VARCHAR(50) PRIMARY KEY
  - `product_category_name_english` VARCHAR(100)
  - `units_sold` INT NOT NULL
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `avg_unit_price` DECIMAL(12, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.dim_products_category_performance`
- **Primary Key**: `product_category_name_english` (VARCHAR(100))
- **Columns**:
  - `product_category_name_english` VARCHAR(100) PRIMARY KEY
  - `units_sold` INT NOT NULL
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `avg_unit_price` DECIMAL(12, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

---

### Finance Mart Tables

#### `serving.fact_payments_method_dist`
- **Primary Key**: `payment_type` (VARCHAR(30))
- **Columns**:
  - `payment_type` VARCHAR(30) PRIMARY KEY
  - `transaction_count` INT NOT NULL
  - `total_payment_value` DECIMAL(12, 2) NOT NULL
  - `average_payment_value` DECIMAL(12, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.fact_payments_installments`
- **Primary Key**: `payment_installments` (INT)
- **Columns**:
  - `payment_installments` INT PRIMARY KEY
  - `transaction_count` INT NOT NULL
  - `total_payment_value` DECIMAL(12, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

---

### Logistics Mart Tables

#### `serving.fact_logistics_delivery_by_state`
- **Primary Key**: `customer_state` (VARCHAR(5))
- **Columns**:
  - `customer_state` VARCHAR(5) PRIMARY KEY
  - `avg_delivery_duration_days` DECIMAL(8, 2) NOT NULL
  - `avg_estimated_delivery_duration_days` DECIMAL(8, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.fact_logistics_delivery_success_rates`
- **Primary Key**: None (single row lookup)
- **Columns**:
  - `total_orders` INT NOT NULL
  - `delivered_orders` INT NOT NULL
  - `late_delivered_orders` INT NOT NULL
  - `delivery_success_rate` DECIMAL(5, 2) NOT NULL
  - `late_delivery_rate` DECIMAL(5, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

#### `serving.fact_logistics_seller_shipping_perf`
- **Primary Key**: `seller_id` (VARCHAR(50))
- **Columns**:
  - `seller_id` VARCHAR(50) PRIMARY KEY
  - `avg_shipping_duration_days` DECIMAL(8, 2) NOT NULL
  - `late_shipping_rate` DECIMAL(5, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ

---

### Executive Mart Tables

#### `serving.fact_executive_kpis`
- **Primary Key**: None (single row lookup)
- **Columns**:
  - `total_revenue` DECIMAL(12, 2) NOT NULL
  - `total_orders` INT NOT NULL
  - `total_customers` INT NOT NULL
  - `total_products` INT NOT NULL
  - `total_sellers` INT NOT NULL
  - `average_delivery_time_days` DECIMAL(8, 2) NOT NULL
  - `average_review_score` DECIMAL(4, 2) NOT NULL
  - `_loaded_at` TIMESTAMPTZ
