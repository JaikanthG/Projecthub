from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import User

from .schemas import (
    RegisterUser,
    LoginUser,
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    create_password_reset_token,
    verify_password_reset_token
)

from .email_service import send_password_reset_email


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Authentication V2"
)


# ============================================================
# REGISTER
# ============================================================

@app.post("/register")
def register(
    user: RegisterUser,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # CHECK USERNAME
    # --------------------------------------------------------

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # --------------------------------------------------------
    # CHECK EMAIL
    # --------------------------------------------------------

    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # --------------------------------------------------------
    # HASH PASSWORD
    # --------------------------------------------------------

    hashed_password = hash_password(
        user.password
    )

    # --------------------------------------------------------
    # CREATE USER
    # --------------------------------------------------------

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


# ============================================================
# LOGIN
# ============================================================

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

    # --------------------------------------------------------
    # ACTIVE CHECK
    # --------------------------------------------------------

    if hasattr(user, "is_active"):

        if user.is_active is False:

            raise HTTPException(
                status_code=403,
                detail="This user account is inactive"
            )

    # --------------------------------------------------------
    # VERIFY PASSWORD
    # --------------------------------------------------------

    password_valid = verify_password(
        login.password,
        user.password
    )

    if not password_valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    # --------------------------------------------------------
    # CREATE JWT
    # --------------------------------------------------------

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


# ============================================================
# GET USERS
# ============================================================

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


# ============================================================
# FORGOT PASSWORD
# ============================================================

@app.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # FIND USER BY EMAIL
    # --------------------------------------------------------

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    # --------------------------------------------------------
    # EMAIL NOT FOUND
    # --------------------------------------------------------

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="Email address not found."
        )

    # --------------------------------------------------------
    # CREATE RESET TOKEN
    # --------------------------------------------------------

    reset_token = create_password_reset_token(
        user_id=user.id,
        email=user.email
    )

    # --------------------------------------------------------
    # SEND EMAIL
    # --------------------------------------------------------

    try:

        send_password_reset_email(
            recipient_email=user.email,
            reset_token=reset_token
        )

    except Exception as e:

        print(
            "Password reset email error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to send password reset email."
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "message": (
            "Password reset instructions "
            "have been sent to your email."
        )
    }


# ============================================================
# RESET PASSWORD
# ============================================================

@app.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # VALIDATE PASSWORD
    # --------------------------------------------------------

    if len(request.new_password) < 6:

        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters."
        )

    # --------------------------------------------------------
    # VERIFY RESET TOKEN
    # --------------------------------------------------------

    token_data = verify_password_reset_token(
        request.token
    )

    user_id = token_data["user_id"]

    email = token_data["email"]

    # --------------------------------------------------------
    # FIND USER
    # --------------------------------------------------------

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    # --------------------------------------------------------
    # EXTRA SECURITY CHECK
    # --------------------------------------------------------

    if user.email.lower() != email.lower():

        raise HTTPException(
            status_code=400,
            detail="Invalid password reset token."
        )

    # --------------------------------------------------------
    # HASH NEW PASSWORD
    # --------------------------------------------------------

    user.password = hash_password(
        request.new_password
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()

    return {
        "message": "Password reset successfully."
    }