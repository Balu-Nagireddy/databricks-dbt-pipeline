from pyspark.sql import DataFrame
from pyspark.sql.functions import col, round, when
from src.pipeline.silver.base import BaseTransformer

class OrdersTransformer(BaseTransformer):
    def __init__(self):
        super().__init__("orders")

    def transform(self, df: DataFrame) -> DataFrame:
        # Trim all strings
        df = self.trim_string_columns(df)
        
        # Normalize status to lowercase
        df = self.normalize_text_column(df, "order_status", uppercase=False)
        
        # Calculate delivery duration in days (if delivered and purchase timestamps are not null)
        # 86400 seconds in a day
        seconds_diff = col("order_delivered_customer_date").cast("long") - col("order_purchase_timestamp").cast("long")
        days_diff = seconds_diff / 86400.0
        
        # Enforce business logic: duration should be positive, else null or 0.
        df = df.withColumn(
            "delivery_duration_days",
            when((days_diff >= 0) & col("order_delivered_customer_date").isNotNull(), round(days_diff, 2))
            .otherwise(None)
        )
        
        # Filter invalid primary keys
        df = df.filter(col("order_id").isNotNull() & (col("order_id") != ""))
        
        return df
