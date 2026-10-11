# routers/dashboard.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# ==========================================
# Dashboard Summary
# ==========================================

@router.get("/summary")
def dashboard_summary(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        data = DashboardService.get_summary(
            current_user,
            db
        )

        return {
            "message": "Dashboard summary retrieved successfully.",
            "data": data
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=403,
            detail=str(e)
        )


# ==========================================
# Project Statistics
# ==========================================

@router.get("/projects")
def project_statistics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        data = DashboardService.get_project_statistics(
            current_user,
            db
        )

        return {
            "message": "Project statistics retrieved successfully.",
            "data": data
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=403,
            detail=str(e)
        )


# ==========================================
# Task Statistics
# ==========================================

@router.get("/tasks")
def task_statistics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        data = DashboardService.get_task_statistics(
            current_user,
            db
        )

        return {
            "message": "Task statistics retrieved successfully.",
            "data": data
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=403,
            detail=str(e)
        )


# ==========================================
# Bug Statistics
# ==========================================

@router.get("/bugs")
def bug_statistics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        data = DashboardService.get_bug_statistics(
            current_user,
            db
        )

        return {
            "message": "Bug statistics retrieved successfully.",
            "data": data
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=403,
            detail=str(e)
        )


# ==========================================
# Knowledge Statistics
# ==========================================

@router.get("/knowledge")
def knowledge_statistics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        data = DashboardService.get_knowledge_statistics(
            current_user,
            db
        )

        return {
            "message": "Knowledge statistics retrieved successfully.",
            "data": data
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=403,
            detail=str(e)
        )