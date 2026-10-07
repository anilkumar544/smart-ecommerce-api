from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Order, Product
from ..schemas import OrderCreate, OrderResponse, OrderStatusUpdate

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == order.product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product.stock < order.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    total_price = product.price * order.quantity

    new_order = Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        status="Pending"
    )

    product.stock -= order.quantity

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order
@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = status_data.status

    db.commit()
    db.refresh(order)

    return order

@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()