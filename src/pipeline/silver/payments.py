from pyspark.sql import DataFrame
from pyspark.sql.functions import col, coalesce, lit
from src.pipeline.silver.base import BaseTransformer

class PaymentsTransformer(BaseTransformer):
    def __init__(self):
        super().__init__("payments")

    def transform(self, df: DataFrame) -> DataFrame:
        # Trim all strings
        df = self.trim_string_columns(df)
        
        # Normalize payment type to lowercase
        df = self.normalize_text_column(df, "payment_type", uppercase=False)
        
        # Clean null values
        df = df.withColumn("payment_installments", coalesce(col("payment_installments"), lit(1)))
        df = df.withColumn("payment_value", coalesce(col("payment_value"), lit(0.0)))
        
        # Filter invalid records (order_id must exist, payment_value cannot be negative)
        df = df.filter(
            col("order_id").isNotNull() & 
            (col("order_id") != "") & 
            (col("payment_value") >= 0)
        )
        
        return df
