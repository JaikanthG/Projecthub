from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..services.activity_service import ActivityService


router = APIRouter(
    prefix="/activities",
    tags=["Activity Logs"]
)


# ==========================================
# Get All Activities
# ==========================================

@router.get("/")
def get_all_activities(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    activities = ActivityService.get_all_activities(
        current_user,
        db
    )

    return {
        "count": len(activities),
        "data": activities
    }


# ==========================================
# Get Activity By ID
# ==========================================

@router.get("/{activity_id}")
def get_activity(
    activity_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return ActivityService.get_activity(
        activity_id,
        current_user,
        db
    )


# ==========================================
# Get Project Activities
# ==========================================

@router.get("/project/{project_id}")
def get_project_activities(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    activities = ActivityService.get_project_activities(
        project_id,
        current_user,
        db
    )

    return {
        "project_id": project_id,
        "count": len(activities),
        "data": activities
    }