from datetime import datetime, timedelta, timezone
import os

from passlib.context import CryptContext
from jose import jwt, JWTError

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends


# ============================================================
# PASSWORD HASHING
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ============================================================
# JWT CONFIGURATION
# ============================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

RESET_TOKEN_EXPIRE_MINUTES = 15


# ============================================================
# PASSWORD FUNCTIONS
# ============================================================

def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# ACCESS TOKEN
# ============================================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ============================================================
# PASSWORD RESET TOKEN
# ============================================================

def create_password_reset_token(
    user_id: int,
    email: str
):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=RESET_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "type": "password_reset",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_password_reset_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # ----------------------------------------------------
        # Make sure this is a password reset token
        # ----------------------------------------------------

        if payload.get("type") != "password_reset":

            raise HTTPException(
                status_code=400,
                detail="Invalid password reset token"
            )

        user_id = payload.get("sub")

        email = payload.get("email")

        if not user_id or not email:

            raise HTTPException(
                status_code=400,
                detail="Invalid password reset token"
            )

        return {
            "user_id": int(user_id),
            "email": email
        }

    except JWTError:

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password reset token"
        )


# ============================================================
# AUTHENTICATION
# ============================================================

security = HTTPBearer()


def verify_token(token: str):

    try:

        print("Received Token:", token)

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("Payload:", payload)

        username = payload.get("sub")

        if username is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

        return username

    except JWTError as e:

        print(
            "JWT Error:",
            str(e)
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    username = verify_token(token)

    return username