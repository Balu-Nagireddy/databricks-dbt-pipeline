from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum, count, countDistinct, avg, lit
from src.pipeline.gold.base import BaseMart

class ExecutiveMart(BaseMart):
    def generate_marts(self) -> dict:
        orders = self.read_silver("orders")
        items = self.read_silver("order_items")
        customers = self.read_silver("customers")
        products = self.read_silver("products")
        sellers = self.read_silver("sellers")
        reviews = self.read_silver("order_reviews")

        # Total revenue
        total_revenue = items.select(sum(col("price") + col("freight_value")).alias("revenue")).first()["revenue"]
        total_orders = orders.count()
        total_customers = customers.select(countDistinct("customer_unique_id").alias("cnt")).first()["cnt"]
        total_products = products.count()
        total_sellers = sellers.count()
        
        avg_delivery = orders.select(avg("delivery_duration_days").alias("avg_del")).first()["avg_del"]
        avg_review = reviews.select(avg("review_score").alias("avg_rev")).first()["avg_rev"]

        # Build single row KPI dataframe using pure JVM expressions to avoid Py4J serialization issues
        kpis = self.spark.range(0, 1).select(
            lit(float(round(total_revenue or 0.0, 2))).alias("total_revenue"),
            lit(int(total_orders)).alias("total_orders"),
            lit(int(total_customers)).alias("total_customers"),
            lit(int(total_products)).alias("total_products"),
            lit(int(total_sellers)).alias("total_sellers"),
            lit(float(round(avg_delivery or 0.0, 2))).alias("average_delivery_time_days"),
            lit(float(round(avg_review or 0.0, 2))).alias("average_review_score")
        )

        return {
            "executive_kpis": kpis
        }
