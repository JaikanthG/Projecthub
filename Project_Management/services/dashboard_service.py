# services/dashboard_service.py

from sqlalchemy.orm import Session

from ..repositories.dashboard_repository import DashboardRepository


class DashboardService:

    # ==========================================
    # Dashboard Summary
    # ==========================================

    @staticmethod
    def get_summary(
        current_user: dict,
        db: Session
    ):

        if current_user["role"].lower() != "admin":
            raise PermissionError(
                "Only Admin can access dashboard."
            )

        return DashboardRepository.get_summary(db)

    # ==========================================
    # Project Statistics
    # ==========================================

    @staticmethod
    def get_project_statistics(
        current_user: dict,
        db: Session
    ):

        if current_user["role"].lower() != "admin":
            raise PermissionError(
                "Only Admin can access dashboard."
            )

        return DashboardRepository.project_statistics(db)

    # ==========================================
    # Task Statistics
    # ==========================================

    @staticmethod
    def get_task_statistics(
        current_user: dict,
        db: Session
    ):

        if current_user["role"].lower() != "admin":
            raise PermissionError(
                "Only Admin can access dashboard."
            )

        return DashboardRepository.task_statistics(db)

    # ==========================================
    # Bug Statistics
    # ==========================================

    @staticmethod
    def get_bug_statistics(
        current_user: dict,
        db: Session
    ):

        if current_user["role"].lower() != "admin":
            raise PermissionError(
                "Only Admin can access dashboard."
            )

        return DashboardRepository.bug_statistics(db)

    # ==========================================
    # Knowledge Statistics
    # ==========================================

    @staticmethod
    def get_knowledge_statistics(
        current_user: dict,
        db: Session
    ):

        if current_user["role"].lower() != "admin":
            raise PermissionError(
                "Only Admin can access dashboard."
            )

        return DashboardRepository.knowledge_statistics(db)