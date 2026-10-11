from pathlib import Path
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from jose import jwt, JWTError

from .database import (
    engine,
    Base,
    get_db,
)

from .models import User

from .schemas import (
    RegisterUser,
    LoginUser,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)


# ============================================================
# ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    BASE_DIR / ".env"
)


# ============================================================
# JWT CONFIGURATION
# ============================================================

# IMPORTANT:
# Replace these with the SAME SECRET_KEY and ALGORITHM
# used by your existing JWT authentication configuration.

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="ProjectHub API",
    description=(
        "Enterprise Engineering Knowledge "
        "and Productivity Platform"
    ),
    version="1.0.0",
)


# ============================================================
# ROUTERS
# ============================================================

from .routers.project import (
    router as project_router,
)

from .routers.project_members import (
    router as project_member_router,
)

from .routers.knowledge import (
    router as knowledge_router,
)

from .routers.bug import (
    router as bug_router,
)

from .routers.task import (
    router as task_router,
)

from .routers.dashboard import (
    router as dashboard_router,
)

from .routers.search import (
    router as search_router,
)

from .routers.document import (
    router as document_router,
)

from .routers.activity import (
    router as activity_router,
)

from .routers.notification import (
    router as notification_router,
)

from .routers.rca import (
    router as rca_router,
)

from .routers.ai import (
    router as ai_router,
)


# ============================================================
# REGISTER ROUTERS
# ============================================================

app.include_router(
    project_router
)

app.include_router(
    project_member_router
)

app.include_router(
    knowledge_router
)

app.include_router(
    bug_router
)

app.include_router(
    task_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    search_router
)

app.include_router(
    document_router
)

app.include_router(
    activity_router
)

app.include_router(
    notification_router
)

app.include_router(
    rca_router
)

app.include_router(
    ai_router
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "ProjectHub API is running",
        "status": "success",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ============================================================
# REGISTER USER
# ============================================================

@app.post("/register")
def register(
    user: RegisterUser,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # Check username
    # --------------------------------------------------------

    existing_user = (
        db.query(User)
        .filter(
            User.username == user.username
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    # --------------------------------------------------------
    # Check email
    # --------------------------------------------------------

    existing_email = (
        db.query(User)
        .filter(
            User.email == user.email
        )
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    # --------------------------------------------------------
    # Hash password
    # --------------------------------------------------------

    hashed_password = hash_password(
        user.password
    )

    # --------------------------------------------------------
    # Create user
    # --------------------------------------------------------

    new_user = User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        role=user.role,
    )

    db.add(
        new_user
    )

    db.commit()

    db.refresh(
        new_user
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "message": "User Registered Successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "role": new_user.role,
        },
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/login")
def login(
    login_data: LoginUser,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # Find user
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.username == login_data.username
        )
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # --------------------------------------------------------
    # Check active status
    # --------------------------------------------------------

    if hasattr(user, "is_active"):

        if not user.is_active:

            raise HTTPException(
                status_code=403,
                detail="User account is inactive",
            )

    # --------------------------------------------------------
    # Verify password
    # --------------------------------------------------------

    password_valid = verify_password(
        login_data.password,
        user.password,
    )

    if not password_valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid Password",
        )

    # --------------------------------------------------------
    # Create JWT
    # --------------------------------------------------------

    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "role": user.role,
        }
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }


# ============================================================
# GET USERS
# ============================================================

@app.get("/users")
def get_users(
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    users = (
        db.query(User)
        .all()
    )

    return {
        "logged_in_user": current_user,
        "users": users,
    }


# ============================================================
# FORGOT PASSWORD
# ============================================================

@app.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # Find user by email
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.email == request.email
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User with this email does not exist",
        )

    # --------------------------------------------------------
    # Create reset-token expiry
    # --------------------------------------------------------

    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=15)
    )

    # --------------------------------------------------------
    # Reset token payload
    # --------------------------------------------------------

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "purpose": "password_reset",
        "exp": expire,
    }

    # --------------------------------------------------------
    # Generate JWT reset token
    # --------------------------------------------------------

    reset_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "message": "Password reset token generated successfully",
        "reset_token": reset_token,
    }


# ============================================================
# RESET PASSWORD
# ============================================================

@app.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # Verify reset token
    # --------------------------------------------------------

    try:

        payload = jwt.decode(
            request.token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        # ----------------------------------------------------
        # Check token purpose
        # ----------------------------------------------------

        if payload.get("purpose") != "password_reset":

            raise HTTPException(
                status_code=400,
                detail="Invalid password reset token",
            )

        # ----------------------------------------------------
        # Get user ID
        # ----------------------------------------------------

        user_id = payload.get("sub")

        if not user_id:

            raise HTTPException(
                status_code=400,
                detail="Invalid password reset token",
            )

    except JWTError:

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password reset token",
        )

    # --------------------------------------------------------
    # Find user
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # --------------------------------------------------------
    # Validate new password
    # --------------------------------------------------------

    if len(request.new_password) < 6:

        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters",
        )

    # --------------------------------------------------------
    # Hash new password
    # --------------------------------------------------------

    user.password = hash_password(
        request.new_password
    )

    # --------------------------------------------------------
    # Save to database
    # --------------------------------------------------------

    db.commit()

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "message": "Password reset successfully",
    }