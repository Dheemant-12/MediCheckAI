from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from jose import jwt

from app.database.dependencies import get_db

from app.models.user_model import User

from app.schemas.symptom_schema import UserSignup

from app.security.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()

@router.post("/signup")
def signup(
    user: UserSignup,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        return {
            "error": "Email already exists"
        }

    hashed_pw = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pw
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:

        return {
            "access_token": "",
            "token_type": "bearer",
            "message": "Invalid email"
        }

    valid_password = verify_password(
        form_data.password,
        existing_user.password
    )

    if not valid_password:

        return {
            "access_token": "",
            "token_type": "bearer",
            "message": "Invalid password"
        }

    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile")
def profile(token: str):

    payload = jwt.decode(
        token,
        "supersecretkey",
        algorithms=["HS256"]
    )

    return {
        "user": payload
    }