from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Cart, Product
from ..schemas import CartCreate, CartResponse

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.post("/", response_model=CartResponse)
def add_to_cart(item: CartCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(
        Product.id == item.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    new_item = Cart(
        user_id=item.user_id,
        product_id=item.product_id,
        quantity=item.quantity
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get("/{user_id}", response_model=list[CartResponse])
def get_cart(user_id: int, db: Session = Depends(get_db)):

    return db.query(Cart).filter(
        Cart.user_id == user_id
    ).all()


@router.delete("/{cart_id}")
def delete_cart_item(cart_id: int, db: Session = Depends(get_db)):

    item = db.query(Cart).filter(
        Cart.id == cart_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Cart item deleted successfully"
    }