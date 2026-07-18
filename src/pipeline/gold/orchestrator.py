import time
from pathlib import Path
from src.config import settings
from src.common.logging import get_logger
from src.pipeline.spark_session import get_spark_session
from src.pipeline.writer import SparkWriter

# Import marts
from src.pipeline.gold.sales import SalesMart
from src.pipeline.gold.customers import CustomersMart
from src.pipeline.gold.products import ProductsMart
from src.pipeline.gold.finance import FinanceMart
from src.pipeline.gold.logistics import LogisticsMart
from src.pipeline.gold.executive import ExecutiveMart
from src.pipeline.gold.quality import BusinessValidationGateway

logger = get_logger(__name__)

class GoldOrchestrator:
    def __init__(self):
        self.spark = get_spark_session("GoldETLJob")
        self.writer = SparkWriter()
        self.gateway = BusinessValidationGateway()

    def run_pipeline(self):
        start_time = time.time()
        logger.info("Starting Gold Analytical Layer Ingestion...")

        # Instantiate marts
        sales_mart = SalesMart(self.spark)
        cust_mart = CustomersMart(self.spark)
        prod_mart = ProductsMart(self.spark)
        fin_mart = FinanceMart(self.spark)
        log_mart = LogisticsMart(self.spark)
        exec_mart = ExecutiveMart(self.spark)

        # Generate analytical dataframes
        all_marts = {}
        
        logger.info("Fleshing out Sales Mart views...")
        all_marts.update(sales_mart.generate_marts())

        logger.info("Fleshing out Customer Mart views...")
        all_marts.update(cust_mart.generate_marts())

        logger.info("Fleshing out Product Mart views...")
        all_marts.update(prod_mart.generate_marts())

        logger.info("Fleshing out Finance Mart views...")
        all_marts.update(fin_mart.generate_marts())

        logger.info("Fleshing out Logistics Mart views...")
        all_marts.update(log_mart.generate_marts())

        logger.info("Fleshing out Executive Mart views...")
        all_marts.update(exec_mart.generate_marts())

        # Validate via Quality Gateway
        logger.info("Verifying metrics consistency via Business Validation Gateway...")
        success = self.gateway.run_validations(all_marts)
        if not success:
            logger.error("WARNING: Some business quality checks FAILED. Check docs/GOLD_DATA_QUALITY.md.")

        # Write output directories
        gold_dir = settings.gold_path
        logger.info(f"Saving Gold Analytical Marts to: {gold_dir}")

        for name, df in all_marts.items():
            # Determine target folder name based on prefix
            if "sales" in name or "revenue" in name or "value" in name:
                folder = "sales"
            elif "customer" in name or "cities" in name or "repeat" in name:
                folder = "customers"
            elif "product" in name or "category" in name:
                folder = "products"
            elif "payment" in name or "transaction" in name or "installment" in name:
                folder = "finance"
            elif "delivery" in name or "shipping" in name or "late" in name:
                folder = "logistics"
            elif "executive" in name or "kpis" in name:
                folder = "executive"
            else:
                folder = "general"

            target_path = gold_dir / folder / name
            self.writer.write_parquet(df, target_path, mode="overwrite")

        elapsed = time.time() - start_time
        logger.info(f"Gold Layer transformation completed in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    orchestrator = GoldOrchestrator()
    try:
        orchestrator.run_pipeline()
    finally:
        orchestrator.spark.stop()
