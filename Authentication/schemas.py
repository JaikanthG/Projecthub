from pydantic import BaseModel, EmailStr


# ============================================================
# REGISTER
# ============================================================

class RegisterUser(BaseModel):

    username: str
    full_name: str
    email: EmailStr
    password: str
    role: str


# ============================================================
# LOGIN
# ============================================================

class LoginUser(BaseModel):

    username: str
    password: str


# ============================================================
# FORGOT PASSWORD
# ============================================================

class ForgotPasswordRequest(BaseModel):

    email: EmailStr


# ============================================================
# RESET PASSWORD
# ============================================================

class ResetPasswordRequest(BaseModel):

    token: str
    new_password: str