from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..services.notification_service import NotificationService


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# ==========================================
# Get My Notifications
# ==========================================

@router.get("/")
def get_my_notifications(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    notifications = NotificationService.get_my_notifications(
        current_user,
        db
    )

    return {
        "count": len(notifications),
        "data": notifications
    }


# ==========================================
# Get My Unread Notifications
# ==========================================

@router.get("/unread")
def get_unread_notifications(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    notifications = NotificationService.get_unread_notifications(
        current_user,
        db
    )

    return {
        "count": len(notifications),
        "data": notifications
    }


# ==========================================
# Get Notification By ID
# ==========================================

@router.get("/{notification_id}")
def get_notification(
    notification_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return NotificationService.get_notification(
        notification_id,
        current_user,
        db
    )


# ==========================================
# Mark Notification As Read
# ==========================================

@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return NotificationService.mark_as_read(
        notification_id,
        current_user,
        db
    )


# ==========================================
# Mark All Notifications As Read
# ==========================================

@router.put("/read-all")
def mark_all_as_read(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return NotificationService.mark_all_as_read(
        current_user,
        db
    )


# ==========================================
# Delete Notification
# ==========================================

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return NotificationService.delete_notification(
        notification_id,
        current_user,
        db
    )