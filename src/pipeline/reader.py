from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
from src.common.logging import get_logger

logger = get_logger(__name__)

class SparkReader:
    """
    Handles read operations from various filesystems and formats.
    """
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def read_csv(self, path: Path, schema=None, header: bool = True, encoding: str = "utf-8") -> DataFrame:
        """
        Reads a CSV file into a Spark DataFrame.
        """
        logger.info(f"Reading CSV from: {path} (encoding: {encoding})")
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found at {path}")

        reader = self.spark.read.option("header", str(header).lower())
        
        # Specify encoding. UTF-8 or Latin1 (ISO-8859-1) are common
        # Spark's CSV reader option is "encoding" or "charset"
        reader = reader.option("encoding", encoding)

        if schema:
            reader = reader.schema(schema)
        else:
            reader = reader.option("inferSchema", "true")

        return reader.csv(str(path))

    def read_parquet(self, path: Path) -> DataFrame:
        """
        Reads a Parquet file/directory into a Spark DataFrame.
        """
        logger.info(f"Reading Parquet from: {path}")
        if not path.exists():
            raise FileNotFoundError(f"Parquet path not found at {path}")
            
        return self.spark.read.parquet(str(path))
