import os
from pathlib import Path
from typing import Dict, Any
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col # Import col explicitly
from src.config import settings
from src.common.logging import get_logger
from src.pipeline.spark_session import get_spark_session
from src.pipeline.reader import SparkReader
from src.pipeline.writer import SparkWriter

# Import transformers
from src.pipeline.silver.customers import CustomersTransformer
from src.pipeline.silver.orders import OrdersTransformer
from src.pipeline.silver.products import ProductsTransformer
from src.pipeline.silver.payments import PaymentsTransformer
from src.pipeline.silver.reviews import ReviewsTransformer
from src.pipeline.silver.sellers import SellersTransformer
from src.pipeline.silver.order_items import OrderItemsTransformer
from src.pipeline.silver.geolocation import GeolocationTransformer

logger = get_logger(__name__)

class SilverPipeline:
    """
    Orchestrates the Silver Layer transformation:
    Reads Bronze data, applies domain cleaners, checks referential integrity,
    writes cleaned Parquet data, and outputs a Data Quality Report.
    """
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.reader = SparkReader(spark)
        self.writer = SparkWriter()
        self.dq_metrics = {}

    def get_bronze_df(self, name: str) -> DataFrame:
        path = settings.bronze_path / name
        return self.reader.read_parquet(path)

    def run_transformations(self):
        logger.info("Starting Silver Layer Transformations...")
        
        # Load Bronze Parquet DataFrames
        bronze_dfs = {
            "customers": self.get_bronze_df("customers"),
            "geolocation": self.get_bronze_df("geolocation"),
            "orders": self.get_bronze_df("orders"),
            "order_items": self.get_bronze_df("order_items"),
            "order_payments": self.get_bronze_df("order_payments"),
            "order_reviews": self.get_bronze_df("order_reviews"),
            "products": self.get_bronze_df("products"),
            "sellers": self.get_bronze_df("sellers"),
            "category_translation": self.get_bronze_df("category_translation")
        }

        # Keep initial row counts for DQ reporting
        for key, df in bronze_dfs.items():
            self.dq_metrics[key] = {
                "input_rows": df.count(),
                "null_imputed": 0,
                "ref_violations": 0,
                "rejected_rows": 0,
                "output_rows": 0
            }

        # --- Transform Geolocation ---
        geo_trans = GeolocationTransformer()
        geo_df = geo_trans.transform(bronze_dfs["geolocation"])
        
        # --- Transform Customers ---
        cust_trans = CustomersTransformer()
        cust_df = cust_trans.transform(bronze_dfs["customers"])

        # --- Transform Sellers ---
        seller_trans = SellersTransformer()
        seller_df = seller_trans.transform(bronze_dfs["sellers"])

        # --- Transform Products ---
        prod_trans = ProductsTransformer()
        # Count null dimensions in products before imputation
        null_dim_count = bronze_dfs["products"].filter(col("product_weight_g").isNull() | col("product_length_cm").isNull()).count()
        self.dq_metrics["products"]["null_imputed"] = null_dim_count
        prod_df = prod_trans.transform(bronze_dfs["products"], bronze_dfs["category_translation"])

        # --- Transform Orders ---
        order_trans = OrdersTransformer()
        order_df = order_trans.transform(bronze_dfs["orders"])

        # --- Transform Order Items ---
        items_trans = OrderItemsTransformer()
        # Null check for price/freight
        null_price_count = bronze_dfs["order_items"].filter(col("price").isNull() | col("freight_value").isNull()).count()
        self.dq_metrics["order_items"]["null_imputed"] = null_price_count
        items_df = items_trans.transform(bronze_dfs["order_items"])

        # --- Transform Payments ---
        pay_trans = PaymentsTransformer()
        null_pay_count = bronze_dfs["order_payments"].filter(col("payment_value").isNull() | col("payment_installments").isNull()).count()
        self.dq_metrics["order_payments"]["null_imputed"] = null_pay_count
        pay_df = pay_trans.transform(bronze_dfs["order_payments"])

        # --- Transform Reviews ---
        rev_trans = ReviewsTransformer()
        rev_df = rev_trans.transform(bronze_dfs["order_reviews"])

        logger.info("Intermediate domain transformations complete. Validating referential integrity...")

        # --- Referential Integrity Checking & Orphan Invalidation ---
        
        # 1. Orders -> Customers (order.customer_id must exist in customers.customer_id)
        cust_ids = cust_df.select("customer_id").distinct()
        order_orphans_df = order_df.join(cust_ids, on="customer_id", how="left_anti")
        order_orphans_cnt = order_orphans_df.count()
        self.dq_metrics["orders"]["ref_violations"] += order_orphans_cnt
        if order_orphans_cnt > 0:
            logger.warning(f"Detected {order_orphans_cnt} orphan orders without valid customer keys.")
        # Filter out orphan orders
        order_df = order_df.join(cust_ids, on="customer_id", how="inner")

        # Get valid orders list
        valid_order_ids = order_df.select("order_id").distinct()

        # 2. Order Items -> Orders (order_items.order_id must exist in orders)
        item_orphans_order_df = items_df.join(valid_order_ids, on="order_id", how="left_anti")
        item_orphans_order_cnt = item_orphans_order_df.count()
        self.dq_metrics["order_items"]["ref_violations"] += item_orphans_order_cnt
        # Filter
        items_df = items_df.join(valid_order_ids, on="order_id", how="inner")

        # 3. Order Items -> Products (order_items.product_id must exist in products)
        valid_prod_ids = prod_df.select("product_id").distinct()
        item_orphans_prod_df = items_df.join(valid_prod_ids, on="product_id", how="left_anti")
        item_orphans_prod_cnt = item_orphans_prod_df.count()
        self.dq_metrics["order_items"]["ref_violations"] += item_orphans_prod_cnt
        # Filter
        items_df = items_df.join(valid_prod_ids, on="product_id", how="inner")

        # 4. Order Items -> Sellers (order_items.seller_id must exist in sellers)
        valid_seller_ids = seller_df.select("seller_id").distinct()
        item_orphans_sell_df = items_df.join(valid_seller_ids, on="seller_id", how="left_anti")
        item_orphans_sell_cnt = item_orphans_sell_df.count()
        self.dq_metrics["order_items"]["ref_violations"] += item_orphans_sell_cnt
        # Filter
        items_df = items_df.join(valid_seller_ids, on="seller_id", how="inner")

        # 5. Payments -> Orders (payments.order_id must exist in orders)
        pay_orphans_df = pay_df.join(valid_order_ids, on="order_id", how="left_anti")
        pay_orphans_cnt = pay_orphans_df.count()
        self.dq_metrics["order_payments"]["ref_violations"] += pay_orphans_cnt
        # Filter
        pay_df = pay_df.join(valid_order_ids, on="order_id", how="inner")

        # 6. Reviews -> Orders (reviews.order_id must exist in orders)
        rev_orphans_df = rev_df.join(valid_order_ids, on="order_id", how="left_anti")
        rev_orphans_cnt = rev_orphans_df.count()
        self.dq_metrics["order_reviews"]["ref_violations"] += rev_orphans_cnt
        # Filter
        rev_df = rev_df.join(valid_order_ids, on="order_id", how="inner")

        # Cleaned outputs to write
        cleaned_dfs = {
            "customers": cust_df,
            "geolocation": geo_df,
            "orders": order_df,
            "order_items": items_df,
            "order_payments": pay_df,
            "order_reviews": rev_df,
            "products": prod_df,
            "sellers": seller_df
        }

        # Compute output counts & rejected rows
        silver_dir = settings.silver_path
        for key, df in cleaned_dfs.items():
            out_cnt = df.count()
            in_cnt = self.dq_metrics[key]["input_rows"]
            
            self.dq_metrics[key]["output_rows"] = out_cnt
            self.dq_metrics[key]["rejected_rows"] = in_cnt - out_cnt
            
            # Write out Parquet file
            self.writer.write_parquet(df, silver_dir / key, mode="overwrite")

        # Also write the category translation cleanly to silver
        self.writer.write_parquet(bronze_dfs["category_translation"], silver_dir / "category_translation", mode="overwrite")
        self.dq_metrics["category_translation"] = {
            "input_rows": bronze_dfs["category_translation"].count(),
            "null_imputed": 0,
            "ref_violations": 0,
            "rejected_rows": 0,
            "output_rows": bronze_dfs["category_translation"].count()
        }

        logger.info("Silver Ingestion and In-Memory transformations successfully stored.")
        self.generate_dq_report()

    def generate_dq_report(self):
        """
        Creates docs/SILVER_DATA_QUALITY.md detailing validation outcomes.
        """
        report_path = Path("./docs/SILVER_DATA_QUALITY.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        md = [
            "# Silver Layer Data Quality Report",
            "",
            "This report documents input/output row metrics, referential integrity violations, and null value handling executed during Silver transforms.",
            "",
            "## Data Validation & Lineage Summary",
            "",
            "| Dataset Name | Input Rows (Bronze) | Output Rows (Silver) | Rejected Rows | Referential Violations | Nulls Imputed |",
            "| :--- | :---: | :---: | :---: | :---: | :---: |"
        ]

        for name, metrics in self.dq_metrics.items():
            md.append(
                f"| {name} | {metrics['input_rows']:,} | {metrics['output_rows']:,} | "
                f"{metrics['rejected_rows']:,} | {metrics['ref_violations']:,} | {metrics['null_imputed']:,} |"
            )

        md.append("")
        md.append("## Business Transformation Rules Applied")
        md.append("1. **Customers**: Standardized states to uppercase, cities to lowercase. Dropped null primary keys.")
        md.append("2. **Orders**: Standardized status. Calculated delivery duration using difference between creation and carrier delivery timestamps.")
        md.append("3. **Products**: Imputed missing physical characteristics (dimensions, photos count, weight) to 0. Joined English translation categories.")
        md.append("4. **Payments**: Normalised type to lowercase. Replaced missing value parameters with defaults. Segregated payments lacking valid orders.")
        md.append("5. **Reviews**: Cleaned text spacing (new line and tabs removals) from comment fields. Removed rows with missing review scores.")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        logger.info(f"Silver Data Quality report generated at: {report_path}")

if __name__ == "__main__":
    spark = get_spark_session("SilverETLJob")
    pipeline = SilverPipeline(spark)
    try:
        pipeline.run_transformations()
    finally:
        spark.stop()
