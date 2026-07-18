"""
Pydantic response schemas for every API domain.
Column names match the actual serving schema in Supabase.
"""
from __future__ import annotations
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ──────────────────────────────────────────────────────────────
# Health
# ──────────────────────────────────────────────────────────────
class HealthResponse(BaseSchema):
    status: str
    database: str
    version: str
    timestamp: datetime


class VersionResponse(BaseSchema):
    name: str
    version: str
    environment: str


# ──────────────────────────────────────────────────────────────
# Executive
# serving.fact_executive_kpis columns:
#   total_revenue, total_orders, total_customers, total_products,
#   total_sellers, average_delivery_time_days, average_review_score
# ──────────────────────────────────────────────────────────────
class ExecutiveKPIResponse(BaseSchema):
    total_revenue: Optional[float] = None
    total_orders: Optional[int] = None
    total_customers: Optional[int] = None
    total_sellers: Optional[int] = None
    total_products: Optional[int] = None
    average_delivery_time_days: Optional[float] = None
    average_review_score: Optional[float] = None


# ──────────────────────────────────────────────────────────────
# Sales
# fact_sales_daily:   sale_date, total_revenue, total_orders
# fact_sales_monthly: sale_month, total_revenue, total_orders
# dim_sales_revenue_by_state: customer_state, total_revenue, total_orders
# ──────────────────────────────────────────────────────────────
class SalesDailyResponse(BaseSchema):
    sale_date: Optional[date] = None
    total_revenue: Optional[float] = None
    total_orders: Optional[int] = None


class SalesMonthlyResponse(BaseSchema):
    sale_month: Optional[date] = None
    total_revenue: Optional[float] = None
    total_orders: Optional[int] = None


class SalesByStateResponse(BaseSchema):
    customer_state: Optional[str] = None
    total_revenue: Optional[float] = None
    total_orders: Optional[int] = None


# ──────────────────────────────────────────────────────────────
# Customers
# dim_customers_clv:       customer_unique_id, total_orders, lifetime_value,
#                          avg_order_spend, is_repeat_customer, customer_segment
# dim_customers_top_cities: customer_city, customer_state, customer_count
# fact_customers_repeat_stats: is_repeat_customer, customer_count
# ──────────────────────────────────────────────────────────────
class CustomerCLVResponse(BaseSchema):
    customer_unique_id: Optional[str] = None
    total_orders: Optional[int] = None
    lifetime_value: Optional[float] = None
    avg_order_spend: Optional[float] = None
    is_repeat_customer: Optional[bool] = None
    customer_segment: Optional[str] = None


class CustomerTopCityResponse(BaseSchema):
    customer_city: Optional[str] = None
    customer_state: Optional[str] = None
    customer_count: Optional[int] = None


class CustomerRepeatStatsResponse(BaseSchema):
    is_repeat_customer: Optional[bool] = None
    customer_count: Optional[int] = None


# ──────────────────────────────────────────────────────────────
# Products
# dim_products_performance: product_id, product_category_name_english,
#                           units_sold, total_revenue, avg_unit_price
# dim_products_category_performance: product_category_name_english,
#                                    units_sold, total_revenue, avg_unit_price
# ──────────────────────────────────────────────────────────────
class ProductPerformanceResponse(BaseSchema):
    product_id: Optional[str] = None
    product_category_name_english: Optional[str] = None
    units_sold: Optional[int] = None
    total_revenue: Optional[float] = None
    avg_unit_price: Optional[float] = None


class ProductCategoryResponse(BaseSchema):
    product_category_name_english: Optional[str] = None
    units_sold: Optional[int] = None
    total_revenue: Optional[float] = None
    avg_unit_price: Optional[float] = None


# ──────────────────────────────────────────────────────────────
# Finance
# fact_payments_method_dist:   payment_type, transaction_count,
#                              total_payment_value, avg_transaction_value
# fact_payments_installments:  payment_installments, transaction_count,
#                              total_payment_value
# ──────────────────────────────────────────────────────────────
class PaymentMethodResponse(BaseSchema):
    payment_type: Optional[str] = None
    transaction_count: Optional[int] = None
    total_payment_value: Optional[float] = None
    avg_transaction_value: Optional[float] = None


class PaymentInstallmentResponse(BaseSchema):
    payment_installments: Optional[int] = None
    transaction_count: Optional[int] = None
    total_payment_value: Optional[float] = None


# ──────────────────────────────────────────────────────────────
# Logistics
# fact_logistics_delivery_by_state: customer_state, avg_delivery_duration_days, total_orders
# fact_logistics_delivery_success_rates: total_orders, total_delivered,
#                                        total_late_orders, success_rate_percent, late_rate_percent
# fact_logistics_seller_shipping_perf: seller_id, items_shipped, avg_shipping_duration_days
# ──────────────────────────────────────────────────────────────
class LogisticsDeliveryByStateResponse(BaseSchema):
    customer_state: Optional[str] = None
    total_orders: Optional[int] = None
    avg_delivery_duration_days: Optional[float] = None


class LogisticsSuccessRatesResponse(BaseSchema):
    total_orders: Optional[int] = None
    total_delivered: Optional[int] = None
    total_late_orders: Optional[int] = None
    success_rate_percent: Optional[float] = None
    late_rate_percent: Optional[float] = None


class LogisticsSellerShippingResponse(BaseSchema):
    seller_id: Optional[str] = None
    items_shipped: Optional[int] = None
    avg_shipping_duration_days: Optional[float] = None
