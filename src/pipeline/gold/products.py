from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum, count, avg, desc, round, broadcast
from src.pipeline.gold.base import BaseMart

class ProductsMart(BaseMart):
    def generate_marts(self) -> dict:
        items = self.read_silver("order_items")
        products = self.read_silver("products")

        # Join items with product dimensions
        prod_sales = items.join(products, on="product_id", how="inner") \
            .withColumn("item_revenue", col("price") + col("freight_value"))

        # Product sales metrics
        product_performance = prod_sales.groupBy("product_id", "product_category_name_english").agg(
            count("order_id").alias("units_sold"),
            round(sum("item_revenue"), 2).alias("total_revenue"),
            round(avg("price"), 2).alias("avg_unit_price")
        ).orderBy(desc("total_revenue"))

        # Category sales metrics
        category_performance = prod_sales.groupBy("product_category_name_english").agg(
            count("order_id").alias("units_sold"),
            round(sum("item_revenue"), 2).alias("total_revenue"),
            round(avg("price"), 2).alias("avg_unit_price")
        ).orderBy(desc("total_revenue"))

        return {
            "product_performance": product_performance,
            "category_performance": category_performance
        }
