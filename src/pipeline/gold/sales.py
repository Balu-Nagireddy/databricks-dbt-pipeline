from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum, count, avg, date_trunc, desc, round, broadcast
from src.pipeline.gold.base import BaseMart

class SalesMart(BaseMart):
    def generate_marts(self) -> dict:
        orders = self.read_silver("orders")
        items = self.read_silver("order_items")
        customers = self.read_silver("customers")
        products = self.read_silver("products")

        # Join datasets to build rich Sales base
        # Use broadcast join on small dimensions: products, customers
        sales_base = items.join(orders, on="order_id", how="inner") \
            .join(customers, on="customer_id", how="inner") \
            .join(products, on="product_id", how="inner") \
            .withColumn("revenue", col("price") + col("freight_value"))

        # 1. Periodical Sales
        daily = sales_base.groupBy(date_trunc("day", col("order_purchase_timestamp")).alias("sale_date")) \
            .agg(
                round(sum("revenue"), 2).alias("total_revenue"),
                count("order_id").alias("total_orders")
            ).orderBy("sale_date")

        weekly = sales_base.groupBy(date_trunc("week", col("order_purchase_timestamp")).alias("sale_week")) \
            .agg(
                round(sum("revenue"), 2).alias("total_revenue"),
                count("order_id").alias("total_orders")
            ).orderBy("sale_week")

        monthly = sales_base.groupBy(date_trunc("month", col("order_purchase_timestamp")).alias("sale_month")) \
            .agg(
                round(sum("revenue"), 2).alias("total_revenue"),
                count("order_id").alias("total_orders")
            ).orderBy("sale_month")

        yearly = sales_base.groupBy(date_trunc("year", col("order_purchase_timestamp")).alias("sale_year")) \
            .agg(
                round(sum("revenue"), 2).alias("total_revenue"),
                count("order_id").alias("total_orders")
            ).orderBy("sale_year")

        # 2. Regional Sales
        by_state = sales_base.groupBy("customer_state").agg(
            round(sum("revenue"), 2).alias("total_revenue"),
            count("order_id").alias("total_orders")
        ).orderBy(desc("total_revenue"))

        by_city = sales_base.groupBy("customer_city", "customer_state").agg(
            round(sum("revenue"), 2).alias("total_revenue"),
            count("order_id").alias("total_orders")
        ).orderBy(desc("total_revenue"))

        # 3. Seller Performance
        by_seller = sales_base.groupBy("seller_id").agg(
            round(sum("revenue"), 2).alias("total_revenue"),
            count("order_id").alias("total_orders")
        ).orderBy(desc("total_revenue"))

        # 4. Product Category
        by_category = sales_base.groupBy("product_category_name_english").agg(
            round(sum("revenue"), 2).alias("total_revenue"),
            count("order_id").alias("total_orders")
        ).orderBy(desc("total_revenue"))

        # 5. Top Products
        top_products = sales_base.groupBy("product_id", "product_category_name_english").agg(
            round(sum("revenue"), 2).alias("total_revenue"),
            count("order_id").alias("total_units_sold")
        ).orderBy(desc("total_revenue"))

        # 6. AOV (Average Order Value)
        aov = sales_base.groupBy("order_id").agg(sum("revenue").alias("order_revenue")) \
            .agg(round(avg("order_revenue"), 2).alias("average_order_value"))

        return {
            "daily_sales": daily,
            "weekly_sales": weekly,
            "monthly_sales": monthly,
            "yearly_sales": yearly,
            "revenue_by_state": by_state,
            "revenue_by_city": by_city,
            "revenue_by_seller": by_seller,
            "revenue_by_category": by_category,
            "top_selling_products": top_products,
            "average_order_value": aov
        }
