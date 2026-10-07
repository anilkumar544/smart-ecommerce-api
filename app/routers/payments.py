from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Payment, Order
from ..schemas import PaymentCreate, PaymentResponse


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# ---------------------------------------------------------
# CREATE PAYMENT
# ---------------------------------------------------------

@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    # Find order
    order = db.query(Order).filter(
        Order.id == payment_data.order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Check if order is already paid
    if order.status == "Paid":
        raise HTTPException(
            status_code=400,
            detail="Order is already paid"
        )

    # Create payment
    payment = Payment(
        order_id=order.id,
        amount=order.total_price,
        payment_method=payment_data.payment_method,
        status="Success"
    )

    # Update order status
    order.status = "Paid"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


# ---------------------------------------------------------
# GET ALL PAYMENTS
# ---------------------------------------------------------

@router.get("/", response_model=list[PaymentResponse])
def get_payments(
    db: Session = Depends(get_db)
):
    return db.query(Payment).all()


# ---------------------------------------------------------
# GET PAYMENT BY ID
# ---------------------------------------------------------

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


# ---------------------------------------------------------
# MOCK PAYMENT
# ---------------------------------------------------------

@router.post("/mock/{order_id}")
def mock_payment(
    order_id: int,
    db: Session = Depends(get_db)
):
    # Find order
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Check if already paid
    if order.status == "Paid":
        raise HTTPException(
            status_code=400,
            detail="Order is already paid"
        )

    # Create mock payment
    payment = Payment(
        order_id=order.id,
        amount=order.total_price,
        payment_method="Mock Card",
        status="Success"
    )

    # Mark order as paid
    order.status = "Paid"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "message": "Mock payment successful",
        "payment_id": payment.id,
        "order_id": order.id,
        "amount": order.total_price,
        "payment_method": "Mock Card",
        "status": "Success"
    }