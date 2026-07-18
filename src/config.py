import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class AppSettings(BaseModel):
    app_name: str = Field(default_factory=lambda: os.getenv("APP_NAME", "databricks-dbt-pipeline"))
    app_env: str = Field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "true").lower() == "true")
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    
    # Spark
    spark_app_name: str = Field(default_factory=lambda: os.getenv("SPARK_APP_NAME", "DataEngineeringPipeline"))
    spark_master: str = Field(default_factory=lambda: os.getenv("SPARK_MASTER", "local[*]"))
    
    # Paths
    raw_data_path: str = Field(default_factory=lambda: os.getenv("RAW_DATA_PATH", "./data/raw"))
    bronze_data_path: str = Field(default_factory=lambda: os.getenv("BRONZE_DATA_PATH", "./data/bronze"))
    silver_data_path: str = Field(default_factory=lambda: os.getenv("SILVER_DATA_PATH", "./data/silver"))
    gold_data_path: str = Field(default_factory=lambda: os.getenv("GOLD_DATA_PATH", "./data/gold"))

    # Database (Supabase)
    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    jdbc_url: str = Field(default_factory=lambda: os.getenv("JDBC_URL", ""))

    @property
    def raw_path(self) -> Path:
        return Path(self.raw_data_path)

    @property
    def bronze_path(self) -> Path:
        return Path(self.bronze_data_path)

    @property
    def silver_path(self) -> Path:
        return Path(self.silver_data_path)

    @property
    def gold_path(self) -> Path:
        return Path(self.gold_data_path)

# Singleton configuration instance
settings = AppSettings()
