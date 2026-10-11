from pydantic import BaseModel
from pydantic import EmailStr

class RegisterUser(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str
    role: str

class LoginUser(BaseModel):
    username: str
    password: str