from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Notification


class NotificationRepository:

    @staticmethod
    def create_notification(
        user_id: int,
        project_id: int,
        title: str,
        message: str,
        notification_type: str,
        db: Session
    ):

        notification = Notification(
            user_id=user_id,
            project_id=project_id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    @staticmethod
    def get_user_notifications(
        user_id: int,
        db: Session
    ):

        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id
            )
            .order_by(
                Notification.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_unread_notifications(
        user_id: int,
        db: Session
    ):

        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
            .order_by(
                Notification.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_notification(
        notification_id: int,
        user_id: int,
        db: Session
    ):

        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
            .first()
        )

        if notification is None:
            raise HTTPException(
                status_code=404,
                detail="Notification not found."
            )

        return notification

    @staticmethod
    def mark_as_read(
        notification_id: int,
        user_id: int,
        db: Session
    ):

        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
            .first()
        )

        if notification is None:
            raise HTTPException(
                status_code=404,
                detail="Notification not found."
            )

        notification.is_read = True

        db.commit()
        db.refresh(notification)

        return notification

    @staticmethod
    def mark_all_as_read(
        user_id: int,
        db: Session
    ):

        notifications = (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
            .all()
        )

        for notification in notifications:
            notification.is_read = True

        db.commit()

        return {
            "message": "All notifications marked as read."
        }

    @staticmethod
    def delete_notification(
        notification_id: int,
        user_id: int,
        db: Session
    ):

        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
            .first()
        )

        if notification is None:
            raise HTTPException(
                status_code=404,
                detail="Notification not found."
            )

        db.delete(notification)
        db.commit()

        return {
            "message": "Notification deleted successfully."
        }