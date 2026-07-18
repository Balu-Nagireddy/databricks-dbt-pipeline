from pyspark.sql import SparkSession, DataFrame
from src.config import settings
from src.common.logging import get_logger

logger = get_logger(__name__)

class BaseMart:
    """
    Abstract Base Class for all Gold domain analytical marts.
    """
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def read_silver(self, name: str) -> DataFrame:
        """
        Helper to read a clean Parquet dataset from the Silver layer.
        """
        path = settings.silver_path / name
        logger.info(f"Reading Silver dataset: {name} from {path}")
        return self.spark.read.parquet(str(path))
        
    def generate_mart(self, *args, **kwargs) -> DataFrame:
        raise NotImplementedError("Subclasses must implement generate_mart method.")
