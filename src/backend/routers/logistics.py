"""
Logistics performance endpoints.
Columns per introspection:
  - fact_logistics_delivery_by_state: customer_state, avg_delivery_duration_days, total_orders
  - fact_logistics_delivery_success_rates: total_orders, total_delivered, total_late_orders,
                                           success_rate_percent, late_rate_percent
  - fact_logistics_seller_shipping_perf: seller_id, items_shipped, avg_shipping_duration_days
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.backend.database import get_db
from src.backend.dependencies import pagination_params
from src.backend.schemas import (
    LogisticsDeliveryByStateResponse,
    LogisticsSuccessRatesResponse,
    LogisticsSellerShippingResponse,
)

router = APIRouter(prefix="/logistics", tags=["Logistics"])


@router.get(
    "/performance",
    response_model=List[LogisticsDeliveryByStateResponse],
    summary="Delivery performance by state",
    description="Returns per-state average delivery duration and order count.",
)
def get_delivery_by_state(db: Session = Depends(get_db), pagination: dict = Depends(pagination_params)):
    rows = db.execute(
        text("SELECT customer_state, total_orders, avg_delivery_duration_days FROM serving.fact_logistics_delivery_by_state ORDER BY avg_delivery_duration_days ASC LIMIT :limit OFFSET :offset;"),
        pagination,
    ).mappings().fetchall()
    return [LogisticsDeliveryByStateResponse(**dict(r)) for r in rows]


@router.get(
    "/success-rates",
    response_model=LogisticsSuccessRatesResponse,
    summary="Platform-wide delivery success rate",
    description="Returns aggregate on-time vs. late delivery statistics.",
)
def get_success_rates(db: Session = Depends(get_db)):
    row = db.execute(
        text("SELECT total_orders, total_delivered, total_late_orders, success_rate_percent, late_rate_percent FROM serving.fact_logistics_delivery_success_rates LIMIT 1;")
    ).mappings().fetchone()
    if row is None:
        return LogisticsSuccessRatesResponse()
    return LogisticsSuccessRatesResponse(**dict(row))


@router.get(
    "/seller-shipping",
    response_model=List[LogisticsSellerShippingResponse],
    summary="Seller shipping performance",
    description="Returns per-seller shipping duration and shipment counts.",
)
def get_seller_shipping(db: Session = Depends(get_db), pagination: dict = Depends(pagination_params)):
    rows = db.execute(
        text("SELECT seller_id, items_shipped, avg_shipping_duration_days FROM serving.fact_logistics_seller_shipping_perf ORDER BY avg_shipping_duration_days ASC NULLS LAST LIMIT :limit OFFSET :offset;"),
        pagination,
    ).mappings().fetchall()
    return [LogisticsSellerShippingResponse(**dict(r)) for r in rows]
