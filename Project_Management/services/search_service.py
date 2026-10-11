from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..repositories.search_repository import SearchRepository


class SearchService:

    # ==========================================
    # Global Search
    # ==========================================

    @staticmethod
    def global_search(
        keyword: str,
        current_user: dict,
        db: Session
    ):

        if not keyword.strip():
            raise HTTPException(
                status_code=400,
                detail="Search keyword cannot be empty."
            )

        return SearchRepository.global_search(
            keyword,
            db
        )

    # ==========================================
    # Knowledge Search
    # ==========================================

    @staticmethod
    def search_knowledge(
        keyword: str,
        current_user: dict,
        db: Session
    ):

        if not keyword.strip():
            raise HTTPException(
                status_code=400,
                detail="Search keyword cannot be empty."
            )

        return SearchRepository.search_knowledge(
            keyword,
            db
        )

    # ==========================================
    # Bug Search
    # ==========================================

    @staticmethod
    def search_bugs(
        keyword: str,
        current_user: dict,
        db: Session
    ):

        if not keyword.strip():
            raise HTTPException(
                status_code=400,
                detail="Search keyword cannot be empty."
            )

        return SearchRepository.search_bugs(
            keyword,
            db
        )

    # ==========================================
    # Task Search
    # ==========================================

    @staticmethod
    def search_tasks(
        keyword: str,
        current_user: dict,
        db: Session
    ):

        if not keyword.strip():
            raise HTTPException(
                status_code=400,
                detail="Search keyword cannot be empty."
            )

        return SearchRepository.search_tasks(
            keyword,
            db
        )

    # ==========================================
    # Filter Search
    # ==========================================

    @staticmethod
    def filter_search(
        project_name: str,
        keyword: str,
        current_user: dict,
        db: Session
    ):

        if not keyword.strip():
            raise HTTPException(
                status_code=400,
                detail="Search keyword cannot be empty."
            )

        if not project_name.strip():
            raise HTTPException(
                status_code=400,
                detail="Project name cannot be empty."
            )

        return SearchRepository.filter_search(
            project_name,
            keyword,
            db
        )