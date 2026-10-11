from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..schemas import (
    CreateBug,
    UpdateBug,
    AssignBug,
    UpdateBugStatus
)

from ..services.bug_service import BugService


router = APIRouter(
    prefix="/bugs",
    tags=["Bug Repository"]
)


# ==========================================
# Create Bug
# ==========================================

@router.post("/")
def create_bug(
    bug: CreateBug,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    created_bug = BugService.create_bug(
        bug,
        current_user,
        db
    )

    return {
        "message": "Bug created successfully.",
        "data": created_bug
    }


# ==========================================
# Get All Bugs
# ==========================================

@router.get("/")
def get_all_bugs(
    project_id: int = Query(
        ...,
        description="Current project ID"
    ),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    bugs = BugService.get_all_bugs(
        project_id,
        current_user,
        db
    )

    return {
        "count": len(bugs),
        "data": bugs
    }


# ==========================================
# Get Bug By ID
# ==========================================

@router.get("/{bug_id}")
def get_bug_by_id(
    bug_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return BugService.get_bug_by_id(
        bug_id,
        current_user,
        db
    )


# ==========================================
# Update Bug
# ==========================================

@router.put("/{bug_id}")
def update_bug(
    bug_id: int,
    bug: UpdateBug,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    updated_bug = BugService.update_bug(
        bug_id,
        bug,
        current_user,
        db
    )

    return {
        "message": "Bug updated successfully.",
        "data": updated_bug
    }


# ==========================================
# Delete Bug
# ==========================================

@router.delete("/{bug_id}")
def delete_bug(
    bug_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return BugService.delete_bug(
        bug_id,
        current_user,
        db
    )


# ==========================================
# Assign Bug
# ==========================================

@router.put("/{bug_id}/assign")
def assign_bug(
    bug_id: int,
    assign: AssignBug,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    assigned_bug = BugService.assign_bug(
        bug_id,
        assign,
        current_user,
        db
    )

    return {
        "message": "Bug assigned successfully.",
        "data": assigned_bug
    }


# ==========================================
# Update Bug Status
# ==========================================

@router.put("/{bug_id}/status")
def update_bug_status(
    bug_id: int,
    status: UpdateBugStatus,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    updated_bug = BugService.update_status(
        bug_id,
        status,
        current_user,
        db
    )

    return {
        "message": "Bug status updated successfully.",
        "data": updated_bug
    }