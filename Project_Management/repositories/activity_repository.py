from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import ActivityLog


class ActivityRepository:

    @staticmethod
    def create_activity(
        project_id: int,
        user_id: int,
        action: str,
        entity_type: str,
        entity_id: int,
        description: str,
        db: Session
    ):

        activity = ActivityLog(
            project_id=project_id,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description
        )

        db.add(activity)
        db.commit()
        db.refresh(activity)

        return activity

    @staticmethod
    def get_all_activities(
        db: Session
    ):

        return (
            db.query(ActivityLog)
            .order_by(
                ActivityLog.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_activity(
        activity_id: int,
        db: Session
    ):

        activity = (
            db.query(ActivityLog)
            .filter(
                ActivityLog.id == activity_id
            )
            .first()
        )

        if activity is None:
            raise HTTPException(
                status_code=404,
                detail="Activity not found."
            )

        return activity

    @staticmethod
    def get_project_activities(
        project_id: int,
        db: Session
    ):

        return (
            db.query(ActivityLog)
            .filter(
                ActivityLog.project_id == project_id
            )
            .order_by(
                ActivityLog.created_at.desc()
            )
            .all()
        )