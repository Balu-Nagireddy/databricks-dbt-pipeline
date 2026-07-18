from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim, lower, upper
from src.common.logging import get_logger

logger = get_logger(__name__)

class BaseTransformer:
    """
    Abstract Base Class for all Silver domain transformers.
    """
    def __init__(self, name: str):
        self.name = name

    def transform(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError("Subclasses must implement the transform method.")

    @staticmethod
    def trim_string_columns(df: DataFrame) -> DataFrame:
        """
        Trims leading and trailing whitespace from all string columns in the DataFrame.
        """
        string_cols = [f.name for f in df.schema.fields if str(f.dataType) == "StringType"]
        for col_name in string_cols:
            df = df.withColumn(col_name, trim(col(col_name)))
        return df

    @staticmethod
    def normalize_text_column(df: DataFrame, col_name: str, uppercase: bool = False) -> DataFrame:
        """
        Trims and standardizes casing of a string column.
        """
        if col_name in df.columns:
            fn = upper if uppercase else lower
            df = df.withColumn(col_name, fn(trim(col(col_name))))
        return df
