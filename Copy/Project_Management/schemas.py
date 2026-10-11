from pydantic import BaseModel
from pydantic import EmailStr


# ==========================
# Register
# ==========================

class RegisterUser(BaseModel):

    username: str

    full_name: str

    email: EmailStr

    password: str

    role: str


# ==========================
# Login
# ==========================

class LoginUser(BaseModel):

    username: str

    password: str


# ==========================
# Create Project
# ==========================

class CreateProject(BaseModel):

    project_name: str

    description: str

    technology_stack: str

    status: str


# ==========================
# Update Project
# ==========================

class UpdateProject(BaseModel):

    project_name: str

    description: str

    technology_stack: str

    status: str


# ==========================
# Project Response
# ==========================

class ProjectResponse(BaseModel):

    id: int

    project_name: str

    description: str

    technology_stack: str

    status: str

    created_by: int

    class Config:
        from_attributes = True