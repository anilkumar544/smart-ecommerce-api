from pydantic import BaseModel, EmailStr


# =========================
# USER SCHEMAS
# =========================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class EditProfile(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


# =========================
# PRODUCT SCHEMAS
# =========================

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    category: str


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    category: str | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    stock: int
    category: str

    class Config:
        from_attributes = True


# =========================
# ORDER SCHEMAS
# =========================

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str

    class Config:
        from_attributes = True


# =========================
# CART SCHEMAS
# =========================

class CartCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


# =========================
# CATEGORY SCHEMAS
# =========================

class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# =========================
# PAYMENT SCHEMAS
# =========================

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    status: str

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str