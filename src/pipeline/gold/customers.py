from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum, count, countDistinct, avg, desc, round, when, lit
from src.pipeline.gold.base import BaseMart

class CustomersMart(BaseMart):
    def generate_marts(self) -> dict:
        orders = self.read_silver("orders")
        items = self.read_silver("order_items")
        customers = self.read_silver("customers")

        # Join orders and items to get revenue by order
        order_revenues = items.groupBy("order_id").agg(sum(col("price") + col("freight_value")).alias("order_value"))
        
        # Link back to customer profile
        customer_orders = orders.join(order_revenues, on="order_id", how="inner") \
            .join(customers, on="customer_id", how="inner")

        # Aggregate at customer_unique_id level
        clv = customer_orders.groupBy("customer_unique_id").agg(
            countDistinct("order_id").alias("total_orders"),
            round(sum("order_value"), 2).alias("lifetime_value"),
            round(avg("order_value"), 2).alias("avg_order_spend")
        ).withColumn(
            "is_repeat_customer",
            when(col("total_orders") > 1, lit(True)).otherwise(lit(False))
        ).withColumn(
            "customer_segment",
            when(col("lifetime_value") > 500.0, lit("VIP"))
            .when(col("lifetime_value") > 150.0, lit("High Value"))
            .otherwise(lit("Standard"))
        ).orderBy(desc("lifetime_value"))

        # Top customer cities
        top_cities = customers.groupBy("customer_city", "customer_state").agg(
            count("customer_id").alias("customer_count")
        ).orderBy(desc("customer_count"))

        # Repeat customer ratio summary
        repeat_stats = clv.groupBy("is_repeat_customer").agg(
            count("customer_unique_id").alias("customer_count")
        )

        return {
            "customer_lifetime_value": clv,
            "top_customer_cities": top_cities,
            "repeat_customer_stats": repeat_stats
        }
