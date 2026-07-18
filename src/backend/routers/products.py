"""
Product analytics endpoints.
Reads from serving.dim_products_performance, dim_products_category_performance.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.backend.database import get_db
from src.backend.dependencies import pagination_params
from src.backend.schemas import ProductPerformanceResponse, ProductCategoryResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    "/top",
    response_model=List[ProductPerformanceResponse],
    summary="Top performing products by revenue",
    description="Returns products ranked by total revenue. Optionally filter by category.",
)
def get_top_products(
    category: Optional[str] = Query(default=None, description="Filter by product category name (English)."),
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
):
    if category:
        rows = db.execute(
            text("SELECT product_id, product_category_name_english, units_sold, total_revenue, avg_unit_price FROM serving.dim_products_performance WHERE product_category_name_english ILIKE :category ORDER BY total_revenue DESC LIMIT :limit OFFSET :offset;"),
            {"category": f"%{category}%", **pagination},
        ).mappings().fetchall()
    else:
        rows = db.execute(
            text("SELECT product_id, product_category_name_english, units_sold, total_revenue, avg_unit_price FROM serving.dim_products_performance ORDER BY total_revenue DESC LIMIT :limit OFFSET :offset;"),
            pagination,
        ).mappings().fetchall()
    return [ProductPerformanceResponse(**dict(r)) for r in rows]


@router.get(
    "/categories",
    response_model=List[ProductCategoryResponse],
    summary="Product category performance",
    description="Returns all product categories ranked by total revenue.",
)
def get_category_performance(db: Session = Depends(get_db), pagination: dict = Depends(pagination_params)):
    rows = db.execute(
        text("SELECT product_category_name_english, units_sold, total_revenue, avg_unit_price FROM serving.dim_products_category_performance ORDER BY total_revenue DESC LIMIT :limit OFFSET :offset;"),
        pagination,
    ).mappings().fetchall()
    return [ProductCategoryResponse(**dict(r)) for r in rows]
