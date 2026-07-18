"""
Executive KPI endpoints.
Reads from serving.fact_executive_kpis.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.backend.database import get_db
from src.backend.schemas import ExecutiveKPIResponse

router = APIRouter(prefix="/executive", tags=["Executive"])


@router.get(
    "/kpis",
    response_model=ExecutiveKPIResponse,
    summary="Platform executive KPIs",
    description=(
        "Returns aggregate platform-level business metrics: total revenue, "
        "orders, customers, sellers, products, average order value, review score, "
        "and on-time delivery rate."
    ),
)
def get_executive_kpis(db: Session = Depends(get_db)):
    row = db.execute(
        text(
            "SELECT total_revenue, total_orders, total_customers, total_products, "
            "total_sellers, average_delivery_time_days, average_review_score "
            "FROM serving.fact_executive_kpis LIMIT 1;"
        )
    ).mappings().fetchone()
    if row is None:
        return ExecutiveKPIResponse()
    return ExecutiveKPIResponse(**dict(row))
