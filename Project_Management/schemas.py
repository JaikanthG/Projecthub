from datetime import datetime

from pydantic import BaseModel, EmailStr


# ==========================================================
# Authentication Schemas
# ==========================================================

class RegisterUser(BaseModel):

    username: str

    full_name: str

    email: EmailStr

    password: str

    role: str = "Employee"


class CreateEmployee(BaseModel):

    username: str

    full_name: str

    email: EmailStr

    password: str


class LoginUser(BaseModel):

    username: str

    password: str


# ==========================================================
# FORGOT PASSWORD
# ==========================================================

class ForgotPasswordRequest(BaseModel):

    email: EmailStr


# ==========================================================
# RESET PASSWORD
# ==========================================================

class ResetPasswordRequest(BaseModel):

    token: str

    new_password: str


# ==========================================================
# Project Schemas
# ==========================================================

class CreateProject(BaseModel):

    project_name: str

    description: str

    technology_stack: str

    status: str


class UpdateProject(BaseModel):

    project_name: str

    description: str

    technology_stack: str

    status: str


# ==========================================================
# Project Member Schemas
# ==========================================================

class AssignProjectMember(BaseModel):

    project_id: int

    user_id: int

    permission: str


class UpdateProjectMember(BaseModel):

    permission: str


# ==========================================================
# Knowledge Schemas
# ==========================================================

class CreateKnowledge(BaseModel):

    project_id: int

    title: str

    content: str

    tags: str

    version: str

    status: str = "draft"


class UpdateKnowledge(BaseModel):

    title: str

    content: str

    tags: str

    version: str

    status: str


# ==========================================================
# Bug Schemas
# ==========================================================

class CreateBug(BaseModel):

    project_id: int

    title: str

    description: str

    priority: str

    severity: str


class UpdateBug(BaseModel):

    title: str

    description: str

    priority: str

    severity: str

    status: str


class AssignBug(BaseModel):

    assigned_to: int


class UpdateBugStatus(BaseModel):

    status: str


# ==========================================================
# Task Schemas
# ==========================================================

class CreateTask(BaseModel):

    project_id: int

    title: str

    description: str

    priority: str

    due_date: str


class UpdateTask(BaseModel):

    title: str

    description: str

    priority: str

    status: str

    due_date: str


class AssignTask(BaseModel):

    assigned_to: int


class UpdateTaskStatus(BaseModel):

    status: str


# ==========================================================
# Document Schemas
# ==========================================================

class DocumentResponse(BaseModel):

    id: int

    project_id: int

    file_name: str

    file_path: str

    file_type: str

    uploaded_by: int

    uploaded_at: datetime

    class Config:
        from_attributes = True


# ==========================================================
# RCA Report Schemas
# ==========================================================

class CreateRCA(BaseModel):

    bug_id: int

    root_cause: str

    impact: str

    corrective_action: str

    preventive_action: str

    resolution: str

    status: str = "open"


class UpdateRCA(BaseModel):

    root_cause: str

    impact: str

    corrective_action: str

    preventive_action: str

    resolution: str

    status: str


class RCAResponse(BaseModel):

    id: int

    bug_id: int

    project_id: int

    root_cause: str

    impact: str

    corrective_action: str

    preventive_action: str

    resolution: str

    status: str

    created_by: int

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True