from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum, count, avg, desc, round
from src.pipeline.gold.base import BaseMart

class FinanceMart(BaseMart):
    def generate_marts(self) -> dict:
        payments = self.read_silver("order_payments")

        # Payment distribution
        payment_distribution = payments.groupBy("payment_type").agg(
            count("order_id").alias("transaction_count"),
            round(sum("payment_value"), 2).alias("total_payment_value"),
            round(avg("payment_value"), 2).alias("avg_transaction_value")
        ).orderBy(desc("total_payment_value"))

        # Installment analysis
        installments = payments.groupBy("payment_installments").agg(
            count("order_id").alias("transaction_count"),
            round(sum("payment_value"), 2).alias("total_payment_value")
        ).orderBy("payment_installments")

        return {
            "payment_method_distribution": payment_distribution,
            "payment_installments_analysis": installments
        }
