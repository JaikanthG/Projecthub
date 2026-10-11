from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..schemas import (
    CreateRCA,
    UpdateRCA,
    RCAResponse
)

from ..services.rca_service import RCAService


router = APIRouter(
    prefix="/rca",
    tags=["RCA Reports"]
)


# ==========================================
# Create RCA
# ==========================================

@router.post(
    "/",
    response_model=RCAResponse
)
def create_rca(
    rca: CreateRCA,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return RCAService.create_rca(
        rca,
        current_user,
        db
    )


# ==========================================
# Get All RCA Reports
# ==========================================

@router.get(
    "/",
    response_model=list[RCAResponse]
)
def get_all_rcas(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return RCAService.get_all_rcas(
        current_user,
        db
    )


# ==========================================
# Get RCA By Bug
# ==========================================

@router.get(
    "/bug/{bug_id}",
    response_model=RCAResponse
)
def get_rca_by_bug(
    bug_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return RCAService.get_rca_by_bug(
        bug_id,
        current_user,
        db
    )


# ==========================================
# Get RCA By Project
# ==========================================

@router.get(
    "/project/{project_id}",
    response_model=list[RCAResponse]
)
def get_project_rcas(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return RCAService.get_project_rcas(
        project_id,
        current_user,
        db
    )


# ==========================================
# Get RCA By ID
# ==========================================

@router.get(
    "/{rca_id}",
    response_model=RCAResponse
)
def get_rca(
    rca_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return RCAService.get_rca_by_id(
        rca_id,
        current_user,
        db
    )


# ==========================================
# Update RCA
# ==========================================

@router.put(
    "/{rca_id}",
    response_model=RCAResponse
)
def update_rca(
    rca_id: int,
    updated_rca: UpdateRCA,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return RCAService.update_rca(
        rca_id,
        updated_rca,
        current_user,
        db
    )


# ==========================================
# Delete RCA
# ==========================================

@router.delete("/{rca_id}")
def delete_rca(
    rca_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return RCAService.delete_rca(
        rca_id,
        current_user,
        db
    )