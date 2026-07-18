"""
Sales analytics endpoints.
Reads from serving.fact_sales_daily, fact_sales_monthly, dim_sales_revenue_by_state.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.backend.database import get_db
from src.backend.dependencies import pagination_params
from src.backend.schemas import SalesDailyResponse, SalesMonthlyResponse, SalesByStateResponse

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get(
    "/daily",
    response_model=List[SalesDailyResponse],
    summary="Daily sales time-series",
    description="Returns daily revenue and order count ordered by date descending.",
)
def get_daily_sales(db: Session = Depends(get_db), pagination: dict = Depends(pagination_params)):
    rows = db.execute(
        text("SELECT sale_date, total_revenue, total_orders FROM serving.fact_sales_daily ORDER BY sale_date DESC LIMIT :limit OFFSET :offset;"),
        pagination,
    ).mappings().fetchall()
    return [SalesDailyResponse(**dict(r)) for r in rows]


@router.get(
    "/monthly",
    response_model=List[SalesMonthlyResponse],
    summary="Monthly sales aggregates",
    description="Returns monthly aggregated revenue and order metrics ordered by month descending.",
)
def get_monthly_sales(db: Session = Depends(get_db), pagination: dict = Depends(pagination_params)):
    rows = db.execute(
        text("SELECT sale_month, total_revenue, total_orders FROM serving.fact_sales_monthly ORDER BY sale_month DESC LIMIT :limit OFFSET :offset;"),
        pagination,
    ).mappings().fetchall()
    return [SalesMonthlyResponse(**dict(r)) for r in rows]


@router.get(
    "/by-state",
    response_model=List[SalesByStateResponse],
    summary="Revenue breakdown by Brazilian state",
    description="Returns total revenue and order count per customer state.",
)
def get_sales_by_state(db: Session = Depends(get_db), pagination: dict = Depends(pagination_params)):
    rows = db.execute(
        text("SELECT customer_state, total_revenue, total_orders FROM serving.dim_sales_revenue_by_state ORDER BY total_revenue DESC LIMIT :limit OFFSET :offset;"),
        pagination,
    ).mappings().fetchall()
    return [SalesByStateResponse(**dict(r)) for r in rows]
