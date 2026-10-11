from datetime import datetime, timedelta

from jose import jwt, JWTError

from passlib.context import CryptContext

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials


# ==========================================
# JWT Configuration
# ==========================================

SECRET_KEY = "mysecretkey123"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==========================================
# Password Hashing
# ==========================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


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


# ==========================================
# JWT Token Creation
# ==========================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
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


# ==========================================
# JWT Authentication
# ==========================================

security = HTTPBearer()


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        user_id = payload.get("user_id")

        role = payload.get("role")

        if username is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

        return {
            "username": username,
            "user_id": user_id,
            "role": role
        }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )


# ==========================================
# Current Logged In User
# ==========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    current_user = verify_token(token)

    return current_user