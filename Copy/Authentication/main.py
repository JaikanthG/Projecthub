from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import User
from .schemas import RegisterUser, LoginUser
from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication V2"
)


@app.post("/register")
def register(
    user: RegisterUser,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registered Successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "role": new_user.role
        }
    }


@app.post("/login")
def login(
    login: LoginUser,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == login.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    password_valid = verify_password(
        login.password,
        user.password
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }


@app.get("/users")
def get_users(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return {
        "logged_in_user": current_user,
        "users": users
    }