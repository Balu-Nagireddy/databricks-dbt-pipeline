from pyspark.sql import DataFrame
from pyspark.sql.functions import col, avg, sum, count, desc, round, when, lit, broadcast
from src.pipeline.gold.base import BaseMart

class LogisticsMart(BaseMart):
    def generate_marts(self) -> dict:
        orders = self.read_silver("orders")
        items = self.read_silver("order_items")
        customers = self.read_silver("customers")

        # Delivery statistics by state
        orders_cust = orders.join(customers, on="customer_id", how="inner")
        
        delivery_by_state = orders_cust.groupBy("customer_state").agg(
            round(avg("delivery_duration_days"), 2).alias("avg_delivery_duration_days"),
            count("order_id").alias("total_orders")
        ).orderBy("avg_delivery_duration_days")

        # Late delivery analysis
        late_orders = orders.withColumn(
            "is_late",
            when(col("order_delivered_customer_date") > col("order_estimated_delivery_date"), lit(1))
            .otherwise(lit(0))
        ).withColumn(
            "is_delivered",
            when(col("order_status") == "delivered", lit(1)).otherwise(lit(0))
        )

        delivery_success_rates = late_orders.agg(
            count("order_id").alias("total_orders"),
            sum("is_delivered").alias("total_delivered"),
            sum("is_late").alias("total_late_orders")
        ).withColumn(
            "success_rate_percent",
            round((col("total_delivered") / col("total_orders")) * 100, 2)
        ).withColumn(
            "late_rate_percent",
            round((col("total_late_orders") / col("total_delivered")) * 100, 2)
        )

        # Shipping times and stats by seller
        seller_shipping = items.join(orders, on="order_id", how="inner") \
            .groupBy("seller_id").agg(
                count("order_id").alias("items_shipped"),
                round(avg("delivery_duration_days"), 2).alias("avg_shipping_duration_days")
            ).orderBy(desc("items_shipped"))

        return {
            "delivery_by_state": delivery_by_state,
            "delivery_success_rates": delivery_success_rates,
            "seller_shipping_performance": seller_shipping
        }
