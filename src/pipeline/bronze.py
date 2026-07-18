from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit
from src.config import settings
from src.common.logging import get_logger
from src.common.constants import DATASET_FILES, BRONZE_SCHEMAS
from src.pipeline.spark_session import get_spark_session
from src.pipeline.reader import SparkReader
from src.pipeline.writer import SparkWriter
from src.pipeline.validator import SchemaValidator

logger = get_logger(__name__)

class BronzePipeline:
    """
    Executes the ingestion, schema validation, type standardization,
    deduplication, and Parquet persistence for the raw dataset into the Bronze Layer.
    """
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.reader = SparkReader(spark)
        self.writer = SparkWriter()

    def run_ingestion(self):
        logger.info("Starting Bronze Ingestion Pipeline...")
        
        raw_dir = settings.raw_path
        bronze_dir = settings.bronze_path

        for key, filename in DATASET_FILES.items():
            file_path = raw_dir / filename
            target_schema = BRONZE_SCHEMAS.get(key)
            
            logger.info(f"Processing raw dataset: {key} ({filename})")
            
            # Read
            # We load CSV without predefined schema first to validate it and see if types differ,
            # then we apply casts to standardize. Olist files are encoded as utf-8.
            raw_df = self.reader.read_csv(file_path, schema=None, encoding="utf-8")
            
            # Validate
            is_valid = SchemaValidator.validate_schema(raw_df, target_schema, key)
            if not is_valid:
                logger.error(f"Validation FAILED for {key}. Proceeding with best-effort casts.")

            # Standardize and Cast Types
            standardized_df = raw_df
            for field in target_schema.fields:
                if field.name in standardized_df.columns:
                    standardized_df = standardized_df.withColumn(
                        field.name, 
                        standardized_df[field.name].cast(field.dataType)
                    )
            
            # Remove exact duplicates
            initial_count = standardized_df.count()
            deduplicated_df = standardized_df.dropDuplicates()
            final_count = deduplicated_df.count()
            
            removed_duplicates = initial_count - final_count
            if removed_duplicates > 0:
                logger.info(f"Removed {removed_duplicates:,} exact duplicate rows from {key}")

            # Add operational metadata
            processed_df = deduplicated_df \
                .withColumn("_ingested_at", current_timestamp()) \
                .withColumn("_source_file", lit(filename))

            # Write Parquet
            target_path = bronze_dir / key
            self.writer.write_parquet(processed_df, target_path, mode="overwrite")
            
        logger.info("Bronze Ingestion Pipeline completed successfully!")

if __name__ == "__main__":
    spark = get_spark_session("BronzeETLJob")
    pipeline = BronzePipeline(spark)
    try:
        pipeline.run_ingestion()
    finally:
        spark.stop()
