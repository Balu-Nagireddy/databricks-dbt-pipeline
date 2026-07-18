from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from src.pipeline.silver.base import BaseTransformer

class SellersTransformer(BaseTransformer):
    def __init__(self):
        super().__init__("sellers")

    def transform(self, df: DataFrame) -> DataFrame:
        # Trim all strings
        df = self.trim_string_columns(df)
        
        # Normalize casing
        df = self.normalize_text_column(df, "seller_city", uppercase=False)
        df = self.normalize_text_column(df, "seller_state", uppercase=True)
        
        # Filter invalid primary keys
        df = df.filter(col("seller_id").isNotNull() & (col("seller_id") != ""))
        
        return df
