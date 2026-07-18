from pyspark.sql import DataFrame
from pyspark.sql.functions import col, coalesce, lit
from src.pipeline.silver.base import BaseTransformer

class OrderItemsTransformer(BaseTransformer):
    def __init__(self):
        super().__init__("order_items")

    def transform(self, df: DataFrame) -> DataFrame:
        # Trim all strings
        df = self.trim_string_columns(df)
        
        # Clean null values
        df = df.withColumn("price", coalesce(col("price"), lit(0.0)))
        df = df.withColumn("freight_value", coalesce(col("freight_value"), lit(0.0)))
        
        # Filter invalid primary/foreign keys
        df = df.filter(
            col("order_id").isNotNull() & (col("order_id") != "") &
            col("product_id").isNotNull() & (col("product_id") != "") &
            col("seller_id").isNotNull() & (col("seller_id") != "")
        )
        
        return df
