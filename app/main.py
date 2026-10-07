from fastapi import FastAPI

from app.database import engine, Base
from app.routers import auth
from app.routers import products
from app.routers import orders
from app.routers import cart
from app.routers import payments

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart E-Commerce API",
    description="FastAPI backend for Smart E-Commerce Platform",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(payments.router)
