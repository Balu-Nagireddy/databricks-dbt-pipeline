from pyspark.sql import DataFrame
from pyspark.sql.functions import col, coalesce, lit
from src.pipeline.silver.base import BaseTransformer

class ProductsTransformer(BaseTransformer):
    def __init__(self):
        super().__init__("products")

    def transform(self, df: DataFrame, translation_df: DataFrame = None) -> DataFrame:
        # Trim all strings
        df = self.trim_string_columns(df)
        
        # Normalize category names to lowercase
        df = self.normalize_text_column(df, "product_category_name", uppercase=False)
        
        # Impute missing values for descriptions, dimensions, and weights with default fallbacks
        df = df.withColumn("product_name_lenght", coalesce(col("product_name_lenght"), lit(0)))
        df = df.withColumn("product_description_lenght", coalesce(col("product_description_lenght"), lit(0)))
        df = df.withColumn("product_photos_qty", coalesce(col("product_photos_qty"), lit(0)))
        df = df.withColumn("product_weight_g", coalesce(col("product_weight_g"), lit(0)))
        df = df.withColumn("product_length_cm", coalesce(col("product_length_cm"), lit(0)))
        df = df.withColumn("product_height_cm", coalesce(col("product_height_cm"), lit(0)))
        df = df.withColumn("product_width_cm", coalesce(col("product_width_cm"), lit(0)))

        # Translate category name if translations are available
        if translation_df is not None:
            # Clean translation dataframe category names as well
            clean_translation = self.trim_string_columns(translation_df)
            clean_translation = self.normalize_text_column(clean_translation, "product_category_name", uppercase=False)
            clean_translation = clean_translation.drop("_ingested_at", "_source_file")
            
            df = df.join(clean_translation, on="product_category_name", how="left")
            
            # Default missing translations to 'unknown' or the original name
            df = df.withColumn(
                "product_category_name_english",
                coalesce(col("product_category_name_english"), col("product_category_name"), lit("unknown"))
            )
        else:
            df = df.withColumn("product_category_name_english", lit("unknown"))
            
        # Filter invalid primary keys
        df = df.filter(col("product_id").isNotNull() & (col("product_id") != ""))
        
        return df
