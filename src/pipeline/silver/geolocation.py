from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from src.pipeline.silver.base import BaseTransformer

class GeolocationTransformer(BaseTransformer):
    def __init__(self):
        super().__init__("geolocation")

    def transform(self, df: DataFrame) -> DataFrame:
        # Trim all strings
        df = self.trim_string_columns(df)
        
        # Normalize casing
        df = self.normalize_text_column(df, "geolocation_city", uppercase=False)
        df = self.normalize_text_column(df, "geolocation_state", uppercase=True)
        
        # Filter invalid records
        df = df.filter(
            col("geolocation_zip_code_prefix").isNotNull() & 
            col("geolocation_lat").isNotNull() & 
            col("geolocation_lng").isNotNull()
        )
        
        return df
