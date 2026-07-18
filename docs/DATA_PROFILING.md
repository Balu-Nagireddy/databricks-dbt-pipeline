# Data Profiling Report

This report contains metadata, structural definitions, validation metrics, and data quality metrics of the acquired dataset.

## Dataset Details
- **Dataset ID**: `olistbr/brazilian-ecommerce`
- **Acquisition Method**: `kagglehub`

## File Validation Summary
| File Name | Encoding | Rows | Columns |
| :--- | :--- | :--- | :--- |
| olist_customers_dataset.csv | utf-8 | 99,441 | 5 |
| olist_geolocation_dataset.csv | utf-8 | 1,000,163 | 5 |
| olist_orders_dataset.csv | utf-8 | 99,441 | 8 |
| olist_order_items_dataset.csv | utf-8 | 112,650 | 7 |
| olist_order_payments_dataset.csv | utf-8 | 103,886 | 5 |
| olist_order_reviews_dataset.csv | utf-8 | 99,224 | 7 |
| olist_products_dataset.csv | utf-8 | 32,951 | 9 |
| olist_sellers_dataset.csv | utf-8 | 3,095 | 4 |
| product_category_name_translation.csv | utf-8 | 71 | 2 |

## Column & Data Quality Details
### olist_customers_dataset.csv
- **Encoding**: utf-8
- **Total Rows**: 99,441
- **Total Columns**: 5

#### Schema & Missing Values
| Column Name | Missing Values Count | Missing % |
| :--- | :---: | :---: |
| `customer_id` | 0 | 0.00% |
| `customer_unique_id` | 0 | 0.00% |
| `customer_zip_code_prefix` | 0 | 0.00% |
| `customer_city` | 0 | 0.00% |
| `customer_state` | 0 | 0.00% |

### olist_geolocation_dataset.csv
- **Encoding**: utf-8
- **Total Rows**: 1,000,163
- **Total Columns**: 5

#### Schema & Missing Values
| Column Name | Missing Values Count | Missing % |
| :--- | :---: | :---: |
| `geolocation_zip_code_prefix` | 0 | 0.00% |
| `geolocation_lat` | 0 | 0.00% |
| `geolocation_lng` | 0 | 0.00% |
| `geolocation_city` | 0 | 0.00% |
| `geolocation_state` | 0 | 0.00% |

### olist_orders_dataset.csv
- **Encoding**: utf-8
- **Total Rows**: 99,441
- **Total Columns**: 8

#### Schema & Missing Values
| Column Name | Missing Values Count | Missing % |
| :--- | :---: | :---: |
| `order_id` | 0 | 0.00% |
| `customer_id` | 0 | 0.00% |
| `order_status` | 0 | 0.00% |
| `order_purchase_timestamp` | 0 | 0.00% |
| `order_approved_at` | 160 | 0.16% |
| `order_delivered_carrier_date` | 1,783 | 1.79% |
| `order_delivered_customer_date` | 2,965 | 2.98% |
| `order_estimated_delivery_date` | 0 | 0.00% |

### olist_order_items_dataset.csv
- **Encoding**: utf-8
- **Total Rows**: 112,650
- **Total Columns**: 7

#### Schema & Missing Values
| Column Name | Missing Values Count | Missing % |
| :--- | :---: | :---: |
| `order_id` | 0 | 0.00% |
| `order_item_id` | 0 | 0.00% |
| `product_id` | 0 | 0.00% |
| `seller_id` | 0 | 0.00% |
| `shipping_limit_date` | 0 | 0.00% |
| `price` | 0 | 0.00% |
| `freight_value` | 0 | 0.00% |

### olist_order_payments_dataset.csv
- **Encoding**: utf-8
- **Total Rows**: 103,886
- **Total Columns**: 5

#### Schema & Missing Values
| Column Name | Missing Values Count | Missing % |
| :--- | :---: | :---: |
| `order_id` | 0 | 0.00% |
| `payment_sequential` | 0 | 0.00% |
| `payment_type` | 0 | 0.00% |
| `payment_installments` | 0 | 0.00% |
| `payment_value` | 0 | 0.00% |

### olist_order_reviews_dataset.csv
- **Encoding**: utf-8
- **Total Rows**: 99,224
- **Total Columns**: 7

#### Schema & Missing Values
| Column Name | Missing Values Count | Missing % |
| :--- | :---: | :---: |
| `review_id` | 0 | 0.00% |
| `order_id` | 0 | 0.00% |
| `review_score` | 0 | 0.00% |
| `review_comment_title` | 87,656 | 88.34% |
| `review_comment_message` | 58,247 | 58.70% |
| `review_creation_date` | 0 | 0.00% |
| `review_answer_timestamp` | 0 | 0.00% |

### olist_products_dataset.csv
- **Encoding**: utf-8
- **Total Rows**: 32,951
- **Total Columns**: 9

#### Schema & Missing Values
| Column Name | Missing Values Count | Missing % |
| :--- | :---: | :---: |
| `product_id` | 0 | 0.00% |
| `product_category_name` | 610 | 1.85% |
| `product_name_lenght` | 610 | 1.85% |
| `product_description_lenght` | 610 | 1.85% |
| `product_photos_qty` | 610 | 1.85% |
| `product_weight_g` | 2 | 0.01% |
| `product_length_cm` | 2 | 0.01% |
| `product_height_cm` | 2 | 0.01% |
| `product_width_cm` | 2 | 0.01% |

### olist_sellers_dataset.csv
- **Encoding**: utf-8
- **Total Rows**: 3,095
- **Total Columns**: 4

#### Schema & Missing Values
| Column Name | Missing Values Count | Missing % |
| :--- | :---: | :---: |
| `seller_id` | 0 | 0.00% |
| `seller_zip_code_prefix` | 0 | 0.00% |
| `seller_city` | 0 | 0.00% |
| `seller_state` | 0 | 0.00% |

### product_category_name_translation.csv
- **Encoding**: utf-8
- **Total Rows**: 71
- **Total Columns**: 2

#### Schema & Missing Values
| Column Name | Missing Values Count | Missing % |
| :--- | :---: | :---: |
| `product_category_name` | 0 | 0.00% |
| `product_category_name_english` | 0 | 0.00% |
