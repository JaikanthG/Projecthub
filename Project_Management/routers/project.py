from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..schemas import (
    CreateProject,
    UpdateProject
)

from ..services.project_service import ProjectService


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/projects",
    tags=["Project Management"]
)


# ============================================================
# CREATE PROJECT
# ============================================================

@router.post("/")
def create_project(
    project: CreateProject,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    new_project = ProjectService.create_project(
        project,
        current_user,
        db
    )

    return {
        "message": "Project created successfully.",
        "project": new_project
    }


# ============================================================
# GET ALL PROJECTS
# ============================================================

@router.get("/")
def get_projects(
    db: Session = Depends(
        get_db
    ),
    current_user: dict = Depends(
        get_current_user
    )
):

    projects = ProjectService.get_all_projects(
        db
    )

    return {
        "count": len(projects),
        "projects": projects
    }


# ============================================================
# GET PROJECT BY ID
# ============================================================

@router.get("/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(
        get_db
    ),
    current_user: dict = Depends(
        get_current_user
    )
):

    return ProjectService.get_project_by_id(
        project_id,
        db
    )


# ============================================================
# UPDATE PROJECT
# ============================================================

@router.put("/{project_id}")
def update_project(
    project_id: int,
    updated_project: UpdateProject,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    project = ProjectService.update_project(
        project_id,
        updated_project,
        current_user,
        db
    )

    return {
        "message": "Project updated successfully.",
        "project": project
    }


# ============================================================
# DELETE PROJECT
# ============================================================

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    return ProjectService.delete_project(
        project_id,
        current_user,
        db
    )