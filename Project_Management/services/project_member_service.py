from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import ProjectMember

from ..repositories.project_member_repository import (
    ProjectMemberRepository
)

from ..repositories.activity_repository import (
    ActivityRepository
)

from ..repositories.notification_repository import (
    NotificationRepository
)

from ..utils.permissions import (
    require_admin
)


class ProjectMemberService:

    # ==========================================
    # Assign Member
    # ==========================================

    @staticmethod
    def assign_member(
        member,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Only Admin Can Assign
        # ==========================================

        require_admin(
            current_user
        )

        # ==========================================
        # Check Project
        # ==========================================

        project = ProjectMemberRepository.get_project(
            member.project_id,
            db
        )

        if project is None:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        # ==========================================
        # Check User
        # ==========================================

        user = ProjectMemberRepository.get_user(
            member.user_id,
            db
        )

        if user is None:

            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        # ==========================================
        # Check Duplicate Assignment
        # ==========================================

        existing_member = (
            ProjectMemberRepository.get_existing_member(
                member.project_id,
                member.user_id,
                db
            )
        )

        if existing_member:

            raise HTTPException(
                status_code=400,
                detail="User already assigned to this project."
            )

        # ==========================================
        # Convert Permission To Lowercase
        # ==========================================

        permission = member.permission.lower()

        # ==========================================
        # Validate Permission
        # ==========================================

        if permission not in [
            "member",
            "contributor"
        ]:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Permission must be either "
                    "'member' or 'contributor'."
                )
            )

        # ==========================================
        # Create Member
        # ==========================================

        new_member = ProjectMember(
            project_id=member.project_id,
            user_id=member.user_id,
            permission=permission,
            assigned_by=current_user["user_id"]
        )

        created_member = (
            ProjectMemberRepository.assign_member(
                new_member,
                db
            )
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=member.project_id,
            user_id=current_user["user_id"],
            action="ASSIGN",
            entity_type="PROJECT_MEMBER",
            entity_id=created_member.id,
            description=(
                f"Assigned user '{user.username}' "
                f"to project '{project.project_name}' "
                f"as {permission}"
            ),
            db=db
        )

        # ==========================================
        # Notification
        # ==========================================

        NotificationRepository.create_notification(
            user_id=member.user_id,
            project_id=member.project_id,
            title="Project Assignment",
            message=(
                f"You have been added to project "
                f"'{project.project_name}' as {permission}."
            ),
            notification_type="PROJECT_ASSIGNMENT",
            db=db
        )

        return created_member


    # ==========================================
    # Get Project Members
    # ==========================================

    @staticmethod
    def get_project_members(
        project_id: int,
        db: Session
    ):

        project = ProjectMemberRepository.get_project(
            project_id,
            db
        )

        if project is None:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        return ProjectMemberRepository.get_project_members(
            project_id,
            db
        )


    # ==========================================
    # Update Permission
    # ==========================================

    @staticmethod
    def update_permission(
        member_id: int,
        updated_member,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Only Admin Can Update
        # ==========================================

        require_admin(
            current_user
        )

        member = ProjectMemberRepository.get_member(
            member_id,
            db
        )

        if member is None:

            raise HTTPException(
                status_code=404,
                detail="Project member not found."
            )

        # ==========================================
        # Convert Permission To Lowercase
        # ==========================================

        permission = updated_member.permission.lower()

        # ==========================================
        # Validate Permission
        # ==========================================

        if permission not in [
            "member",
            "contributor"
        ]:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Permission must be either "
                    "'member' or 'contributor'."
                )
            )

        old_permission = member.permission

        member.permission = permission

        ProjectMemberRepository.update_member(
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=member.project_id,
            user_id=current_user["user_id"],
            action="UPDATE_PERMISSION",
            entity_type="PROJECT_MEMBER",
            entity_id=member.id,
            description=(
                f"Changed project member permission "
                f"from '{old_permission}' to '{permission}'"
            ),
            db=db
        )

        # ==========================================
        # Notification
        # ==========================================

        NotificationRepository.create_notification(
            user_id=member.user_id,
            project_id=member.project_id,
            title="Project Permission Updated",
            message=(
                f"Your project permission has been changed "
                f"from '{old_permission}' to '{permission}'."
            ),
            notification_type="PERMISSION_CHANGE",
            db=db
        )

        return member


    # ==========================================
    # Remove Member
    # ==========================================

    @staticmethod
    def remove_member(
        member_id: int,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Only Admin Can Remove
        # ==========================================

        require_admin(
            current_user
        )

        member = ProjectMemberRepository.get_member(
            member_id,
            db
        )

        if member is None:

            raise HTTPException(
                status_code=404,
                detail="Project member not found."
            )

        # ==========================================
        # Store Information Before Delete
        # ==========================================

        project_id = member.project_id
        user_id = member.user_id

        ProjectMemberRepository.delete_member(
            member,
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=project_id,
            user_id=current_user["user_id"],
            action="REMOVE",
            entity_type="PROJECT_MEMBER",
            entity_id=member_id,
            description=(
                f"Removed user {user_id} "
                f"from project"
            ),
            db=db
        )

        # ==========================================
        # Notification
        # ==========================================

        NotificationRepository.create_notification(
            user_id=user_id,
            project_id=project_id,
            title="Project Membership Removed",
            message=(
                "You have been removed from the project."
            ),
            notification_type="PROJECT_REMOVAL",
            db=db
        )

        return {
            "message": "Project member removed successfully."
        }