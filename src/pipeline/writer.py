from pathlib import Path
from typing import List
from pyspark.sql import DataFrame
from src.common.logging import get_logger

logger = get_logger(__name__)

class SparkWriter:
    """
    Handles write operations for Spark DataFrames.
    """
    def __init__(self):
        pass

    def write_parquet(self, df: DataFrame, path: Path, mode: str = "overwrite", partition_by: List[str] = None):
        """
        Saves a Spark DataFrame as Parquet.
        """
        logger.info(f"Writing Parquet file to: {path} (mode: {mode})")
        
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        writer = df.write.mode(mode)
        
        if partition_by:
            logger.info(f"Partitioning output by: {partition_by}")
            writer = writer.partitionBy(*partition_by)
            
        writer.parquet(str(path))
        logger.info(f"Successfully saved Parquet dataset to {path}")
