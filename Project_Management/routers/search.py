# routers/search.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..services.search_service import SearchService


router = APIRouter(
    prefix="/search",
    tags=["Global Search"]
)


# ==========================================
# Global Search
# ==========================================

@router.get("/")
def global_search(
    q: str = Query(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    results = SearchService.global_search(
        q,
        current_user,
        db
    )

    return {
        "keyword": q,
        "data": results
    }


# ==========================================
# Knowledge Search
# ==========================================

@router.get("/knowledge")
def search_knowledge(
    q: str = Query(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    results = SearchService.search_knowledge(
        q,
        current_user,
        db
    )

    return {
        "keyword": q,
        "count": len(results),
        "data": results
    }


# ==========================================
# Bug Search
# ==========================================

@router.get("/bugs")
def search_bugs(
    q: str = Query(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    results = SearchService.search_bugs(
        q,
        current_user,
        db
    )

    return {
        "keyword": q,
        "count": len(results),
        "data": results
    }


# ==========================================
# Task Search
# ==========================================

@router.get("/tasks")
def search_tasks(
    q: str = Query(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    results = SearchService.search_tasks(
        q,
        current_user,
        db
    )

    return {
        "keyword": q,
        "count": len(results),
        "data": results
    }


# ==========================================
# Filter Search
# ==========================================

@router.get("/filter")
def filter_search(
    project: str = Query(
        ...,
        description="Project Name"
    ),
    q: str = Query(
        ...,
        description="Search Keyword"
    ),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    results = SearchService.filter_search(
        project,
        q,
        current_user,
        db
    )

    return {
        "project": project,
        "keyword": q,
        "data": results
    }