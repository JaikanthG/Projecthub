from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..repositories.notification_repository import NotificationRepository


class NotificationService:

    # ==========================================
    # Create Notification
    # ==========================================

    @staticmethod
    def create_notification(
        user_id: int,
        project_id: int,
        title: str,
        message: str,
        notification_type: str,
        current_user: dict,
        db: Session
    ):

        if not title.strip():
            raise HTTPException(
                status_code=400,
                detail="Notification title cannot be empty."
            )

        if not message.strip():
            raise HTTPException(
                status_code=400,
                detail="Notification message cannot be empty."
            )

        if not notification_type.strip():
            raise HTTPException(
                status_code=400,
                detail="Notification type cannot be empty."
            )

        return NotificationRepository.create_notification(
            user_id=user_id,
            project_id=project_id,
            title=title,
            message=message,
            notification_type=notification_type,
            db=db
        )

    # ==========================================
    # Get My Notifications
    # ==========================================

    @staticmethod
    def get_my_notifications(
        current_user: dict,
        db: Session
    ):

        user_id = current_user.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in authentication token."
            )

        return NotificationRepository.get_user_notifications(
            user_id,
            db
        )

    # ==========================================
    # Get My Unread Notifications
    # ==========================================

    @staticmethod
    def get_unread_notifications(
        current_user: dict,
        db: Session
    ):

        user_id = current_user.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in authentication token."
            )

        return NotificationRepository.get_unread_notifications(
            user_id,
            db
        )

    # ==========================================
    # Get Notification By ID
    # ==========================================

    @staticmethod
    def get_notification(
        notification_id: int,
        current_user: dict,
        db: Session
    ):

        user_id = current_user.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in authentication token."
            )

        return NotificationRepository.get_notification(
            notification_id,
            user_id,
            db
        )

    # ==========================================
    # Mark Notification As Read
    # ==========================================

    @staticmethod
    def mark_as_read(
        notification_id: int,
        current_user: dict,
        db: Session
    ):

        user_id = current_user.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in authentication token."
            )

        return NotificationRepository.mark_as_read(
            notification_id,
            user_id,
            db
        )

    # ==========================================
    # Mark All As Read
    # ==========================================

    @staticmethod
    def mark_all_as_read(
        current_user: dict,
        db: Session
    ):

        user_id = current_user.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in authentication token."
            )

        return NotificationRepository.mark_all_as_read(
            user_id,
            db
        )

    # ==========================================
    # Delete Notification
    # ==========================================

    @staticmethod
    def delete_notification(
        notification_id: int,
        current_user: dict,
        db: Session
    ):

        user_id = current_user.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in authentication token."
            )

        return NotificationRepository.delete_notification(
            notification_id,
            user_id,
            db
        )