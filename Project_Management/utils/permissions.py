from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import ProjectMember


# ============================================================
# Require Admin
# ============================================================

def require_admin(
    current_user: dict
):
    """
    Admin-only operation.

    Allowed:
        Admin

    Not allowed:
        Employee
        Employee + Contributor
        Employee + Member
    """

    role = str(
        current_user.get("role", "")
    ).lower()

    if role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Only Admin can perform this operation."
        )


# ============================================================
# Require Contributor Or Admin
# ============================================================

def require_contributor_or_admin(
    project_id: int,
    current_user: dict,
    db: Session
):
    """
    Allows project modification only to:

        1. Admin
        2. Employee + Contributor

    Denies:

        Employee + Member
        Employee without project membership
    """

    role = str(
        current_user.get("role", "")
    ).lower()

    # --------------------------------------------------------
    # Admin
    # --------------------------------------------------------

    if role == "admin":
        return


    # --------------------------------------------------------
    # Get User ID
    # --------------------------------------------------------

    user_id = current_user.get(
        "user_id"
    )

    if user_id is None:

        raise HTTPException(
            status_code=403,
            detail="User information not found."
        )


    # --------------------------------------------------------
    # Find Project Membership
    # --------------------------------------------------------

    member = db.query(
        ProjectMember
    ).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()


    # --------------------------------------------------------
    # User Not Assigned
    # --------------------------------------------------------

    if member is None:

        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this project."
        )


    # --------------------------------------------------------
    # Check Project Role
    # --------------------------------------------------------

    permission = str(
        member.permission or ""
    ).lower()


    # --------------------------------------------------------
    # Contributor
    # --------------------------------------------------------

    if permission == "contributor":
        return


    # --------------------------------------------------------
    # Member
    # --------------------------------------------------------

    raise HTTPException(
        status_code=403,
        detail=(
            "Only Admin or Contributor can "
            "perform this operation."
        )
    )


# ============================================================
# Require Project Member
# ============================================================

def require_project_member(
    project_id: int,
    current_user: dict,
    db: Session
):
    """
    Read access.

    Admin:
        Full access.

    Employee + Contributor:
        Read access.

    Employee + Member:
        Read access.

    Employee without project membership:
        No project access.
    """

    role = str(
        current_user.get("role", "")
    ).lower()


    # --------------------------------------------------------
    # Admin
    # --------------------------------------------------------

    if role == "admin":
        return


    # --------------------------------------------------------
    # Get User ID
    # --------------------------------------------------------

    user_id = current_user.get(
        "user_id"
    )

    if user_id is None:

        raise HTTPException(
            status_code=403,
            detail="User information not found."
        )


    # --------------------------------------------------------
    # Check Membership
    # --------------------------------------------------------

    member = db.query(
        ProjectMember
    ).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()


    if member is None:

        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this project."
        )


    # --------------------------------------------------------
    # Member OR Contributor
    # --------------------------------------------------------

    permission = str(
        member.permission or ""
    ).lower()

    if permission in [
        "member",
        "contributor"
    ]:
        return


    raise HTTPException(
        status_code=403,
        detail="You do not have access to this project."
    )