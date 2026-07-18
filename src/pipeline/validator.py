from pyspark.sql import DataFrame
from pyspark.sql.types import StructType
from src.common.logging import get_logger

logger = get_logger(__name__)

class SchemaValidator:
    """
    Validates Spark DataFrame schemas against target StructType schemas.
    """
    @staticmethod
    def validate_schema(df: DataFrame, expected_schema: StructType, dataset_name: str) -> bool:
        """
        Validates the schema of a DataFrame against the expected StructType schema.
        Returns True if schema is valid, otherwise False.
        """
        logger.info(f"Starting schema validation for dataset: {dataset_name}")
        
        df_fields = {field.name: field.dataType for field in df.schema.fields}
        expected_fields = {field.name: field.dataType for field in expected_schema.fields}
        
        errors = []
        warnings = []
        
        # 1. Check for missing columns
        for name in expected_fields:
            if name not in df_fields:
                errors.append(f"Missing expected column: '{name}'")
                
        # 2. Check for unexpected columns
        for name in df_fields:
            if name not in expected_fields:
                warnings.append(f"Unexpected column present in data: '{name}'")
                
        # 3. Check for type mismatches
        for name, expected_type in expected_fields.items():
            if name in df_fields:
                actual_type = df_fields[name]
                # Compare string representation of types
                if str(actual_type) != str(expected_type):
                    # We might want to cast types in bronze, so flag as warning if they are castable
                    warnings.append(
                        f"Column type mismatch for '{name}': Expected {expected_type}, got {actual_type}"
                    )
                    
        # Log results
        if warnings:
            for w in warnings:
                logger.warning(f"[{dataset_name} Validation Warning] {w}")
                
        if errors:
            for e in errors:
                logger.error(f"[{dataset_name} Validation Error] {e}")
            return False
            
        logger.info(f"Schema validation PASSED for dataset: {dataset_name}")
        return True
