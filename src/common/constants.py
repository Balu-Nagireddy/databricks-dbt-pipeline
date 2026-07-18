from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
)

# File names mapping
DATASET_FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

# Schemas for raw validation & Bronze ingestion
BRONZE_SCHEMAS = {
    "customers": StructType([
        StructField("customer_id", StringType(), False),
        StructField("customer_unique_id", StringType(), False),
        StructField("customer_zip_code_prefix", IntegerType(), False),
        StructField("customer_city", StringType(), True),
        StructField("customer_state", StringType(), True)
    ]),
    
    "geolocation": StructType([
        StructField("geolocation_zip_code_prefix", IntegerType(), False),
        StructField("geolocation_lat", DoubleType(), True),
        StructField("geolocation_lng", DoubleType(), True),
        StructField("geolocation_city", StringType(), True),
        StructField("geolocation_state", StringType(), True)
    ]),
    
    "orders": StructType([
        StructField("order_id", StringType(), False),
        StructField("customer_id", StringType(), False),
        StructField("order_status", StringType(), True),
        StructField("order_purchase_timestamp", TimestampType(), True),
        StructField("order_approved_at", TimestampType(), True),
        StructField("order_delivered_carrier_date", TimestampType(), True),
        StructField("order_delivered_customer_date", TimestampType(), True),
        StructField("order_estimated_delivery_date", TimestampType(), True)
    ]),
    
    "order_items": StructType([
        StructField("order_id", StringType(), False),
        StructField("order_item_id", IntegerType(), False),
        StructField("product_id", StringType(), False),
        StructField("seller_id", StringType(), False),
        StructField("shipping_limit_date", TimestampType(), True),
        StructField("price", DoubleType(), True),
        StructField("freight_value", DoubleType(), True)
    ]),
    
    "order_payments": StructType([
        StructField("order_id", StringType(), False),
        StructField("payment_sequential", IntegerType(), False),
        StructField("payment_type", StringType(), True),
        StructField("payment_installments", IntegerType(), True),
        StructField("payment_value", DoubleType(), True)
    ]),
    
    "order_reviews": StructType([
        StructField("review_id", StringType(), False),
        StructField("order_id", StringType(), False),
        StructField("review_score", IntegerType(), True),
        StructField("review_comment_title", StringType(), True),
        StructField("review_comment_message", StringType(), True),
        StructField("review_creation_date", TimestampType(), True),
        StructField("review_answer_timestamp", TimestampType(), True)
    ]),
    
    "products": StructType([
        StructField("product_id", StringType(), False),
        StructField("product_category_name", StringType(), True),
        StructField("product_name_lenght", IntegerType(), True),
        StructField("product_description_lenght", IntegerType(), True),
        StructField("product_photos_qty", IntegerType(), True),
        StructField("product_weight_g", IntegerType(), True),
        StructField("product_length_cm", IntegerType(), True),
        StructField("product_height_cm", IntegerType(), True),
        StructField("product_width_cm", IntegerType(), True)
    ]),
    
    "sellers": StructType([
        StructField("seller_id", StringType(), False),
        StructField("seller_zip_code_prefix", IntegerType(), False),
        StructField("seller_city", StringType(), True),
        StructField("seller_state", StringType(), True)
    ]),
    
    "category_translation": StructType([
        StructField("product_category_name", StringType(), False),
        StructField("product_category_name_english", StringType(), True)
    ])
}
