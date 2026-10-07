import bcrypt

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse, LoginRequest, EditProfile
from ..auth_jwt import create_access_token
from ..security import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# REGISTER
# =========================

@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role="customer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================
# LOGIN
# =========================

@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_correct = bcrypt.checkpw(
        user.password.encode("utf-8"),
        existing_user.password.encode("utf-8")
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "user_id": existing_user.id
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": existing_user.id,
        "name": existing_user.name,
        "email": existing_user.email,
        "role": existing_user.role
    }


# =========================
# GET PROFILE
# =========================

@router.get("/profile/{user_id}", response_model=UserResponse)
def get_profile(
    user_id: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can access only your own profile"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# =========================
# EDIT PROFILE
# =========================

@router.put("/edit-profile/{user_id}", response_model=UserResponse)
def edit_profile(
    user_id: int,
    profile: EditProfile,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can edit only your own profile"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if profile.name is not None:
        user.name = profile.name

    if profile.email is not None:
        existing_email = db.query(User).filter(
            User.email == profile.email,
            User.id != user_id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        user.email = profile.email

    db.commit()
    db.refresh(user)

    return user