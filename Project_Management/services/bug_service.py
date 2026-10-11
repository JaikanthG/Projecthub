from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import (
    Bug,
    Project,
    User
)

from ..repositories.bug_repository import (
    BugRepository
)

from ..repositories.activity_repository import (
    ActivityRepository
)

from ..repositories.notification_repository import (
    NotificationRepository
)

from ..utils.permissions import (
    require_admin,
    require_contributor_or_admin
)


class BugService:

    # ==========================================
    # Create Bug
    # ==========================================

    @staticmethod
    def create_bug(
        bug,
        current_user: dict,
        db: Session
    ):

        project = (
            db.query(Project)
            .filter(
                Project.id == bug.project_id
            )
            .first()
        )

        if project is None:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        require_contributor_or_admin(
            bug.project_id,
            current_user,
            db
        )

        existing_bug = (
            BugRepository.get_bug_by_title(
                bug.title,
                db
            )
        )

        if existing_bug:

            raise HTTPException(
                status_code=400,
                detail="Bug title already exists."
            )

        new_bug = Bug(
            project_id=bug.project_id,
            title=bug.title,
            description=bug.description,
            priority=bug.priority.lower(),
            severity=bug.severity.lower(),
            status="open",
            created_by=current_user["user_id"]
        )

        created_bug = BugRepository.create_bug(
            new_bug,
            db
        )

        ActivityRepository.create_activity(
            project_id=created_bug.project_id,
            user_id=current_user["user_id"],
            action="CREATE",
            entity_type="BUG",
            entity_id=created_bug.id,
            description=(
                f"Created bug: "
                f"{created_bug.title}"
            ),
            db=db
        )

        return created_bug

    # ==========================================
    # Get All Bugs
    # ==========================================

    @staticmethod
    def get_all_bugs(
        project_id: int,
        current_user: dict,
        db: Session
    ):

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

        # Admin can view any project.
        # Employee must be assigned to this project.
        require_contributor_or_admin(
            project_id,
            current_user,
            db
        )

        return (
            db.query(Bug)
            .filter(
                Bug.project_id == project_id
            )
            .all()
        )

    # ==========================================
    # Get Bug By ID
    # ==========================================

    @staticmethod
    def get_bug_by_id(
        bug_id: int,
        current_user: dict,
        db: Session
    ):

        bug = BugRepository.get_bug_by_id(
            bug_id,
            db
        )

        if bug is None:

            raise HTTPException(
                status_code=404,
                detail="Bug not found."
            )

        require_contributor_or_admin(
            bug.project_id,
            current_user,
            db
        )

        return bug

    # ==========================================
    # Update Bug
    # ==========================================

    @staticmethod
    def update_bug(
        bug_id: int,
        updated_bug,
        current_user: dict,
        db: Session
    ):

        bug = BugRepository.get_bug_by_id(
            bug_id,
            db
        )

        if bug is None:

            raise HTTPException(
                status_code=404,
                detail="Bug not found."
            )

        require_contributor_or_admin(
            bug.project_id,
            current_user,
            db
        )

        bug.title = updated_bug.title

        bug.description = (
            updated_bug.description
        )

        bug.priority = (
            updated_bug.priority.lower()
        )

        bug.severity = (
            updated_bug.severity.lower()
        )

        bug.status = (
            updated_bug.status.lower()
        )

        BugRepository.update_bug(
            db
        )

        ActivityRepository.create_activity(
            project_id=bug.project_id,
            user_id=current_user["user_id"],
            action="UPDATE",
            entity_type="BUG",
            entity_id=bug.id,
            description=(
                f"Updated bug: "
                f"{bug.title}"
            ),
            db=db
        )

        return bug

    # ==========================================
    # Delete Bug
    # ==========================================

    @staticmethod
    def delete_bug(
        bug_id: int,
        current_user: dict,
        db: Session
    ):

        bug = BugRepository.get_bug_by_id(
            bug_id,
            db
        )

        if bug is None:

            raise HTTPException(
                status_code=404,
                detail="Bug not found."
            )

        require_admin(
            current_user
        )

        ActivityRepository.create_activity(
            project_id=bug.project_id,
            user_id=current_user["user_id"],
            action="DELETE",
            entity_type="BUG",
            entity_id=bug.id,
            description=(
                f"Deleted bug: "
                f"{bug.title}"
            ),
            db=db
        )

        BugRepository.delete_bug(
            bug,
            db
        )

        return {
            "message": "Bug deleted successfully."
        }

    # ==========================================
    # Assign Bug
    # ==========================================

    @staticmethod
    def assign_bug(
        bug_id: int,
        assign,
        current_user: dict,
        db: Session
    ):

        require_admin(
            current_user
        )

        bug = BugRepository.get_bug_by_id(
            bug_id,
            db
        )

        if bug is None:

            raise HTTPException(
                status_code=404,
                detail="Bug not found."
            )

        user = (
            db.query(User)
            .filter(
                User.id == assign.assigned_to
            )
            .first()
        )

        if user is None:

            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        bug.assigned_to = (
            assign.assigned_to
        )

        BugRepository.update_bug(
            db
        )

        ActivityRepository.create_activity(
            project_id=bug.project_id,
            user_id=current_user["user_id"],
            action="ASSIGN",
            entity_type="BUG",
            entity_id=bug.id,
            description=(
                f"Assigned bug "
                f"'{bug.title}' "
                f"to user {user.username}"
            ),
            db=db
        )

        NotificationRepository.create_notification(
            user_id=assign.assigned_to,
            project_id=bug.project_id,
            title="Bug Assigned",
            message=(
                f"You have been assigned bug "
                f"'{bug.title}'."
            ),
            notification_type="BUG_ASSIGNMENT",
            db=db
        )

        return bug

    # ==========================================
    # Update Bug Status
    # ==========================================

    @staticmethod
    def update_status(
        bug_id: int,
        status,
        current_user: dict,
        db: Session
    ):

        bug = BugRepository.get_bug_by_id(
            bug_id,
            db
        )

        if bug is None:

            raise HTTPException(
                status_code=404,
                detail="Bug not found."
            )

        require_contributor_or_admin(
            bug.project_id,
            current_user,
            db
        )

        old_status = bug.status

        bug.status = (
            status.status.lower()
        )

        BugRepository.update_bug(
            db
        )

        ActivityRepository.create_activity(
            project_id=bug.project_id,
            user_id=current_user["user_id"],
            action="STATUS_CHANGE",
            entity_type="BUG",
            entity_id=bug.id,
            description=(
                f"Changed bug "
                f"'{bug.title}' status "
                f"from '{old_status}' "
                f"to '{bug.status}'"
            ),
            db=db
        )

        return bug