from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import (
    RCAReport,
    Bug,
    Project,
    ProjectMember
)

from ..repositories.rca_repository import (
    RCARepository
)

from ..repositories.activity_repository import (
    ActivityRepository
)


class RCAService:

    # ==========================================
    # Project Access Helper
    # ==========================================

    @staticmethod
    def _require_project_access(
        project_id: int,
        current_user: dict,
        db: Session
    ):

        user_id = current_user.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in authentication token."
            )

        global_role = str(
            current_user.get("role", "")
        ).lower()

        # Admin has access to every project
        if global_role == "admin":
            return

        # Check project exists
        project = (
            db.query(Project)
            .filter(
                Project.id == project_id
            )
            .first()
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        # Check project membership
        member = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id
            )
            .first()
        )

        if member is None:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to this project."
            )

    # ==========================================
    # Contributor / Admin Access Helper
    # ==========================================

    @staticmethod
    def _require_contributor_or_admin(
        project_id: int,
        current_user: dict,
        db: Session
    ):

        user_id = current_user.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in authentication token."
            )

        global_role = str(
            current_user.get("role", "")
        ).lower()

        # Admin has full access
        if global_role == "admin":
            return

        # Check project exists
        project = (
            db.query(Project)
            .filter(
                Project.id == project_id
            )
            .first()
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        # Check membership
        member = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id
            )
            .first()
        )

        if member is None:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to this project."
            )

        # Only Contributor can create/update
        if str(member.permission).lower() != "contributor":
            raise HTTPException(
                status_code=403,
                detail="Only Contributor can perform this action."
            )

    # ==========================================
    # Create RCA
    # ==========================================

    @staticmethod
    def create_rca(
        rca,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Check Bug
        # ==========================================

        bug = (
            db.query(Bug)
            .filter(
                Bug.id == rca.bug_id
            )
            .first()
        )

        if bug is None:
            raise HTTPException(
                status_code=404,
                detail="Bug not found."
            )

        # ==========================================
        # Permission Check
        # ==========================================

        RCAService._require_contributor_or_admin(
            bug.project_id,
            current_user,
            db
        )

        # ==========================================
        # Check Existing RCA
        # ==========================================

        existing_rca = RCARepository.get_rca_by_bug(
            rca.bug_id,
            db
        )

        if existing_rca:
            raise HTTPException(
                status_code=400,
                detail="RCA report already exists for this bug."
            )

        # ==========================================
        # Validate Status
        # ==========================================

        status = rca.status.lower()

        allowed_statuses = [
            "open",
            "in_progress",
            "resolved",
            "closed"
        ]

        if status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail=(
                    "RCA status must be one of: "
                    "open, in_progress, resolved, closed."
                )
            )

        # ==========================================
        # Create RCA
        # ==========================================

        new_rca = RCAReport(
            bug_id=bug.id,
            project_id=bug.project_id,
            root_cause=rca.root_cause,
            impact=rca.impact,
            corrective_action=rca.corrective_action,
            preventive_action=rca.preventive_action,
            resolution=rca.resolution,
            status=status,
            created_by=current_user["user_id"]
        )

        created_rca = RCARepository.create_rca(
            new_rca,
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=bug.project_id,
            user_id=current_user["user_id"],
            action="CREATE",
            entity_type="RCA",
            entity_id=created_rca.id,
            description=(
                f"Created RCA report for bug "
                f"'{bug.title}'"
            ),
            db=db
        )

        return created_rca

    # ==========================================
    # Get All RCA Reports
    # ==========================================

    @staticmethod
    def get_all_rcas(
        current_user: dict,
        db: Session
    ):

        global_role = str(
            current_user.get("role", "")
        ).lower()

        # Global RCA listing is Admin-only
        if global_role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Only Admin can access all RCA reports."
            )

        return RCARepository.get_all_rcas(
            db
        )

    # ==========================================
    # Get RCA By ID
    # ==========================================

    @staticmethod
    def get_rca_by_id(
        rca_id: int,
        current_user: dict,
        db: Session
    ):

        rca = RCARepository.get_rca_by_id(
            rca_id,
            db
        )

        if rca is None:
            raise HTTPException(
                status_code=404,
                detail="RCA report not found."
            )

        # Project-level read access
        RCAService._require_project_access(
            rca.project_id,
            current_user,
            db
        )

        return rca

    # ==========================================
    # Get RCA By Bug
    # ==========================================

    @staticmethod
    def get_rca_by_bug(
        bug_id: int,
        current_user: dict,
        db: Session
    ):

        # Check bug first
        bug = (
            db.query(Bug)
            .filter(
                Bug.id == bug_id
            )
            .first()
        )

        if bug is None:
            raise HTTPException(
                status_code=404,
                detail="Bug not found."
            )

        # Project-level read access
        RCAService._require_project_access(
            bug.project_id,
            current_user,
            db
        )

        rca = RCARepository.get_rca_by_bug(
            bug_id,
            db
        )

        if rca is None:
            raise HTTPException(
                status_code=404,
                detail="RCA report not found for this bug."
            )

        return rca

    # ==========================================
    # Get RCA By Project
    # ==========================================

    @staticmethod
    def get_project_rcas(
        project_id: int,
        current_user: dict,
        db: Session
    ):

        # Project-level read access
        RCAService._require_project_access(
            project_id,
            current_user,
            db
        )

        return RCARepository.get_project_rcas(
            project_id,
            db
        )

    # ==========================================
    # Update RCA
    # ==========================================

    @staticmethod
    def update_rca(
        rca_id: int,
        updated_rca,
        current_user: dict,
        db: Session
    ):

        rca = RCARepository.get_rca_by_id(
            rca_id,
            db
        )

        if rca is None:
            raise HTTPException(
                status_code=404,
                detail="RCA report not found."
            )

        # ==========================================
        # Permission Check
        # ==========================================

        RCAService._require_contributor_or_admin(
            rca.project_id,
            current_user,
            db
        )

        # ==========================================
        # Validate Status
        # ==========================================

        status = updated_rca.status.lower()

        allowed_statuses = [
            "open",
            "in_progress",
            "resolved",
            "closed"
        ]

        if status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail=(
                    "RCA status must be one of: "
                    "open, in_progress, resolved, closed."
                )
            )

        # ==========================================
        # Update RCA
        # ==========================================

        rca.root_cause = updated_rca.root_cause
        rca.impact = updated_rca.impact
        rca.corrective_action = updated_rca.corrective_action
        rca.preventive_action = updated_rca.preventive_action
        rca.resolution = updated_rca.resolution
        rca.status = status

        RCARepository.update_rca(
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=rca.project_id,
            user_id=current_user["user_id"],
            action="UPDATE",
            entity_type="RCA",
            entity_id=rca.id,
            description=(
                f"Updated RCA report #{rca.id}"
            ),
            db=db
        )

        return rca

    # ==========================================
    # Delete RCA
    # ==========================================

    @staticmethod
    def delete_rca(
        rca_id: int,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Only Admin Can Delete
        # ==========================================

        if current_user["role"].lower() != "admin":
            raise HTTPException(
                status_code=403,
                detail="Only Admin can delete RCA reports."
            )

        # ==========================================
        # Get RCA
        # ==========================================

        rca = RCARepository.get_rca_by_id(
            rca_id,
            db
        )

        if rca is None:
            raise HTTPException(
                status_code=404,
                detail="RCA report not found."
            )

        project_id = rca.project_id

        # ==========================================
        # Delete RCA
        # ==========================================

        RCARepository.delete_rca(
            rca,
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=project_id,
            user_id=current_user["user_id"],
            action="DELETE",
            entity_type="RCA",
            entity_id=rca_id,
            description=(
                f"Deleted RCA report #{rca_id}"
            ),
            db=db
        )

        return {
            "message": "RCA report deleted successfully."
        }