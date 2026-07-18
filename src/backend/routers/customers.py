"""
Customer analytics endpoints.
Reads from serving.dim_customers_clv, dim_customers_top_cities, fact_customers_repeat_stats.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.backend.database import get_db
from src.backend.dependencies import pagination_params
from src.backend.schemas import CustomerCLVResponse, CustomerTopCityResponse, CustomerRepeatStatsResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get(
    "/segments",
    response_model=List[CustomerCLVResponse],
    summary="Customer lifetime value and segmentation",
    description="Returns customer spend, order count, and segment. Filter by segment: VIP, 'High Value', Standard.",
)
def get_customer_segments(
    segment: Optional[str] = Query(default=None, description="Filter by customer segment."),
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
):
    if segment:
        rows = db.execute(
            text("SELECT customer_unique_id, total_orders, lifetime_value, avg_order_spend, is_repeat_customer, customer_segment FROM serving.dim_customers_clv WHERE customer_segment = :segment ORDER BY lifetime_value DESC LIMIT :limit OFFSET :offset;"),
            {"segment": segment, **pagination},
        ).mappings().fetchall()
    else:
        rows = db.execute(
            text("SELECT customer_unique_id, total_orders, lifetime_value, avg_order_spend, is_repeat_customer, customer_segment FROM serving.dim_customers_clv ORDER BY lifetime_value DESC LIMIT :limit OFFSET :offset;"),
            pagination,
        ).mappings().fetchall()
    return [CustomerCLVResponse(**dict(r)) for r in rows]


@router.get(
    "/top-cities",
    response_model=List[CustomerTopCityResponse],
    summary="Top customer cities by customer count",
    description="Returns cities with their customer count.",
)
def get_top_cities(db: Session = Depends(get_db), pagination: dict = Depends(pagination_params)):
    rows = db.execute(
        text("SELECT customer_city, customer_state, customer_count FROM serving.dim_customers_top_cities ORDER BY customer_count DESC LIMIT :limit OFFSET :offset;"),
        pagination,
    ).mappings().fetchall()
    return [CustomerTopCityResponse(**dict(r)) for r in rows]


@router.get(
    "/repeat-stats",
    response_model=List[CustomerRepeatStatsResponse],
    summary="Repeat vs. one-time customer distribution",
    description="Returns the split between repeat customers and one-time buyers.",
)
def get_repeat_stats(db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT is_repeat_customer, customer_count FROM serving.fact_customers_repeat_stats;")
    ).mappings().fetchall()
    return [CustomerRepeatStatsResponse(**dict(r)) for r in rows]
