from pyspark.sql import DataFrame
from pyspark.sql.functions import col, regexp_replace, coalesce, lit
from src.pipeline.silver.base import BaseTransformer

class ReviewsTransformer(BaseTransformer):
    def __init__(self):
        super().__init__("reviews")

    def transform(self, df: DataFrame) -> DataFrame:
        # Trim all strings
        df = self.trim_string_columns(df)
        
        # Clean comment title and messages (replace tabs/newlines with single space)
        if "review_comment_title" in df.columns:
            df = df.withColumn(
                "review_comment_title", 
                regexp_replace(col("review_comment_title"), r"[\r\n\t]+", " ")
            )
            df = df.withColumn("review_comment_title", coalesce(col("review_comment_title"), lit("")))
            
        if "review_comment_message" in df.columns:
            df = df.withColumn(
                "review_comment_message", 
                regexp_replace(col("review_comment_message"), r"[\r\n\t]+", " ")
            )
            df = df.withColumn("review_comment_message", coalesce(col("review_comment_message"), lit("")))
            
        # Filter invalid review scores and primary keys
        df = df.filter(
            col("review_id").isNotNull() & 
            (col("review_id") != "") & 
            col("review_score").isNotNull()
        )
        
        return df
