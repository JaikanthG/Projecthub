from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..schemas import (
    AssignProjectMember,
    UpdateProjectMember
)

from ..services.project_member_service import ProjectMemberService


router = APIRouter(
    prefix="/project-members",
    tags=["Project Members"]
)


# ==========================================
# Assign Member
# ==========================================

@router.post("/assign")
def assign_member(
    member: AssignProjectMember,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    assigned_member = ProjectMemberService.assign_member(
        member,
        current_user,
        db
    )

    return {
        "message": "Employee assigned successfully.",
        "data": {
            "id": assigned_member.id,
            "project_id": assigned_member.project_id,
            "user_id": assigned_member.user_id,
            "permission": assigned_member.permission,
            "assigned_by": assigned_member.assigned_by
        }
    }


# ==========================================
# Get Project Members
# ==========================================

@router.get("/project/{project_id}")
def get_project_members(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    members = ProjectMemberService.get_project_members(
        project_id,
        db
    )

    result = []

    for member in members:

        result.append({
            "id": member.id,
            "project_id": member.project_id,
            "user_id": member.user_id,
            "permission": member.permission,
            "assigned_by": member.assigned_by
        })

    return {
        "total_members": len(result),
        "members": result
    }


# ==========================================
# Update Permission
# ==========================================

@router.put("/{member_id}")
def update_permission(
    member_id: int,
    member: UpdateProjectMember,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    updated_member = ProjectMemberService.update_permission(
        member_id,
        member,
        current_user,
        db
    )

    return {
        "message": "Permission updated successfully.",
        "data": {
            "id": updated_member.id,
            "project_id": updated_member.project_id,
            "user_id": updated_member.user_id,
            "permission": updated_member.permission,
            "assigned_by": updated_member.assigned_by
        }
    }


# ==========================================
# Remove Member
# ==========================================

@router.delete("/{member_id}")
def remove_member(
    member_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return ProjectMemberService.remove_member(
        member_id,
        current_user,
        db
    )