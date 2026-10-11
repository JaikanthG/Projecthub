import os

from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from passlib.context import CryptContext

from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from .database import get_db
from .models import User
from .schemas import ForgotPasswordRequest, ResetPasswordRequest

from passlib.context import CryptContext

from fastapi import APIRouter
router = APIRouter()

# ==========================================================
# JWT CONFIGURATION
# ==========================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "mysecretkey123"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ==========================================================
# PASSWORD HASHING
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(
    password: str
):

    return pwd_context.hash(
        password
    )


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==========================================================
# JWT TOKEN CREATION
# ==========================================================

def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ==========================================================
# HTTP BEARER AUTHENTICATION
# ==========================================================

security = HTTPBearer()


# ==========================================================
# VERIFY JWT TOKEN
# ==========================================================

def verify_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get(
            "sub"
        )

        user_id = payload.get(
            "user_id"
        )

        role = payload.get(
            "role"
        )

        # ==================================================
        # Validate Username
        # ==================================================

        if username is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token: username missing."
            )

        # ==================================================
        # Validate User ID
        # ==================================================

        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token: user ID missing."
            )

        # ==================================================
        # Validate Role
        # ==================================================

        if role is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token: role missing."
            )

        # ==================================================
        # Return Current User Information
        # ==================================================

        return {
            "username": username,
            "user_id": user_id,
            "role": role
        }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )


# ==========================================================
# CURRENT LOGGED-IN USER
# ==========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):

    token = credentials.credentials

    current_user = verify_token(
        token
    )

    return current_user


# ============================================================
# FORGOT PASSWORD
# ============================================================

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exist"
        )

    # Reset token expires in 15 minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "purpose": "password_reset",
        "exp": expire
    }

    reset_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "Password reset token generated successfully",
        "reset_token": reset_token
    }


# ============================================================
# RESET PASSWORD
# ============================================================

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            request.token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Make sure this token was created specifically
        # for password reset
        if payload.get("purpose") != "password_reset":
            raise HTTPException(
                status_code=400,
                detail="Invalid password reset token"
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="Invalid password reset token"
            )

    except JWTError:

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password reset token"
        )

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if len(request.new_password) < 6:

        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters"
        )

    # Hash the new password
    user.password = pwd_context.hash(
        request.new_password
    )

    db.commit()

    return {
        "message": "Password reset successfully"
    }