from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Project, ProjectMember

from ..repositories.activity_repository import (
    ActivityRepository
)


class ActivityService:

    # ==========================================
    # Project Access Validation
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

        # Global Admin has access to every project
        if global_role == "admin":
            return

        # Verify project exists
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

        # Verify project membership
        membership = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id
            )
            .first()
        )

        if membership is None:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this project."
            )

    # ==========================================
    # Create Activity
    # ==========================================

    @staticmethod
    def create_activity(
        project_id: int,
        action: str,
        entity_type: str,
        entity_id: int,
        description: str,
        current_user: dict,
        db: Session
    ):

        user_id = current_user.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in authentication token."
            )

        if not action.strip():
            raise HTTPException(
                status_code=400,
                detail="Action cannot be empty."
            )

        if not entity_type.strip():
            raise HTTPException(
                status_code=400,
                detail="Entity type cannot be empty."
            )

        if not description.strip():
            raise HTTPException(
                status_code=400,
                detail="Description cannot be empty."
            )

        return ActivityRepository.create_activity(
            project_id=project_id,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            db=db
        )

    # ==========================================
    # Get All Activities
    # ==========================================

    @staticmethod
    def get_all_activities(
        current_user: dict,
        db: Session
    ):

        global_role = str(
            current_user.get("role", "")
        ).lower()

        # Only Admin can access unscoped/all activities.
        if global_role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Only Admin can access all activities."
            )

        return ActivityRepository.get_all_activities(db)

    # ==========================================
    # Get Activity By ID
    # ==========================================

    @staticmethod
    def get_activity(
        activity_id: int,
        current_user: dict,
        db: Session
    ):

        activity = ActivityRepository.get_activity(
            activity_id,
            db
        )

        if activity is None:
            raise HTTPException(
                status_code=404,
                detail="Activity not found."
            )

        ActivityService._require_project_access(
            activity.project_id,
            current_user,
            db
        )

        return activity

    # ==========================================
    # Get Project Activities
    # ==========================================

    @staticmethod
    def get_project_activities(
        project_id: int,
        current_user: dict,
        db: Session
    ):

        ActivityService._require_project_access(
            project_id,
            current_user,
            db
        )

        return ActivityRepository.get_project_activities(
            project_id,
            db
        )