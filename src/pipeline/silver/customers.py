from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from src.pipeline.silver.base import BaseTransformer

class CustomersTransformer(BaseTransformer):
    def __init__(self):
        super().__init__("customers")

    def transform(self, df: DataFrame) -> DataFrame:
        # Trim all strings
        df = self.trim_string_columns(df)
        
        # Normalize casing
        df = self.normalize_text_column(df, "customer_city", uppercase=False)
        df = self.normalize_text_column(df, "customer_state", uppercase=True)
        
        # Filter invalid primary keys
        df = df.filter(col("customer_id").isNotNull() & (col("customer_id") != ""))
        
        return df
