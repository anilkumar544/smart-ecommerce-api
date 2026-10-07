# Smart E-Commerce API

## Project Overview

Smart E-Commerce API is a backend application developed using FastAPI.

The project provides APIs for user authentication, JWT authorization, product management, order management, shopping cart management, and mock payment processing.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- bcrypt
- Swagger UI
- Mock Payment

## Project Features

### Authentication
- User registration
- User login
- JWT token generation
- Protected profile API
- Profile editing
- Password hashing using bcrypt

### Product Management
- Create product
- Get all products
- Get product by ID
- Update product
- Delete product

### Order Management
- Create order
- Get all orders
- Get order by ID
- Update order status
- Automatic stock reduction
- Stock availability validation

### Shopping Cart
- Add product to cart
- View user cart
- Delete cart item

### Payment
- Create payment
- Get payments
- Get payment by ID
- Mock payment processing
- Prevent duplicate payment for the same order

## Database

SQLite database is used for this project.

Database file:

`ecommerce.db`

## API Documentation

After starting the application, Swagger UI is available at:

`http://127.0.0.1:9020/docs`

## How to Run the Project

### 1. Create virtual environment

```bash
python -m venv venv