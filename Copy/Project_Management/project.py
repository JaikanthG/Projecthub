from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Project
from .schemas import CreateProject, UpdateProject
from .auth import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Project Management"]
)


# ==========================================
# Create Project
# ==========================================
@router.post("/")
def create_project(
    project: CreateProject,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    print("Current User:", current_user)

    role = current_user.get("role")

    if role is None:
        raise HTTPException(
            status_code=401,
            detail="Role not found in JWT token."
        )

    if role.strip().lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can create projects."
        )

    existing_project = db.query(Project).filter(
        Project.project_name == project.project_name
    ).first()

    if existing_project:
        raise HTTPException(
            status_code=400,
            detail="Project already exists."
        )

    new_project = Project(
        project_name=project.project_name,
        description=project.description,
        technology_stack=project.technology_stack,
        status=project.status,
        created_by=current_user["user_id"]
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "message": "Project created successfully.",
        "project": new_project
    }


# ==========================================
# Get All Projects
# ==========================================
@router.get("/")
def get_projects(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    projects = db.query(Project).all()

    return {
        "count": len(projects),
        "projects": projects
    }


# ==========================================
# Get Project By ID
# ==========================================
@router.get("/{project_id}")
def get_project(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    return project


# ==========================================
# Update Project
# ==========================================
@router.put("/{project_id}")
def update_project(
    project_id: int,
    updated_project: UpdateProject,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    role = current_user.get("role")

    if role.strip().lower() != "admin":
            raise HTTPException(
                status_code=403,
                detail="Only Admin can create projects."
            )

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    duplicate_project = db.query(Project).filter(
        Project.project_name == updated_project.project_name,
        Project.id != project_id
    ).first()

    if duplicate_project:
        raise HTTPException(
            status_code=400,
            detail="Project name already exists."
        )

    project.project_name = updated_project.project_name
    project.description = updated_project.description
    project.technology_stack = updated_project.technology_stack
    project.status = updated_project.status

    db.commit()
    db.refresh(project)

    return {
        "message": "Project updated successfully.",
        "project": project
    }


# ==========================================
# Delete Project
# ==========================================
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    role = current_user.get("role")

    if role.strip().lower() != "admin":
                raise HTTPException(
                    status_code=403,
                    detail="Only Admin can create projects."
                )

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully."
    }