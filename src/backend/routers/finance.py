"""
Finance / payments analytics endpoints.
Reads from serving.fact_payments_method_dist, fact_payments_installments.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.backend.database import get_db
from src.backend.schemas import PaymentMethodResponse, PaymentInstallmentResponse

router = APIRouter(prefix="/finance", tags=["Finance"])


@router.get(
    "/payments",
    response_model=List[PaymentMethodResponse],
    summary="Payment method distribution",
    description="Returns breakdown of payment types with transaction counts and payment values.",
)
def get_payment_methods(db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT payment_type, transaction_count, total_payment_value, avg_transaction_value FROM serving.fact_payments_method_dist ORDER BY total_payment_value DESC;")
    ).mappings().fetchall()
    return [PaymentMethodResponse(**dict(r)) for r in rows]


@router.get(
    "/installments",
    response_model=List[PaymentInstallmentResponse],
    summary="Installment payment analysis",
    description="Returns the breakdown of transactions by number of installments and payment values.",
)
def get_installments(db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT payment_installments, transaction_count, total_payment_value FROM serving.fact_payments_installments ORDER BY payment_installments ASC;")
    ).mappings().fetchall()
    return [PaymentInstallmentResponse(**dict(r)) for r in rows]
