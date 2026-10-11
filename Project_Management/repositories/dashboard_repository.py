from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import (
    User,
    Project,
    ProjectMember,
    Knowledge,
    Bug,
    Task
)


class DashboardRepository:

    @staticmethod
    def get_summary(
        db: Session
    ):

        return {
            "total_users":
                db.query(
                    func.count(User.id)
                ).scalar(),

            "total_projects":
                db.query(
                    func.count(Project.id)
                ).scalar(),

            "total_project_members":
                db.query(
                    func.count(ProjectMember.id)
                ).scalar(),

            "total_knowledge":
                db.query(
                    func.count(Knowledge.id)
                ).scalar(),

            "total_bugs":
                db.query(
                    func.count(Bug.id)
                ).scalar(),

            "total_tasks":
                db.query(
                    func.count(Task.id)
                ).scalar()
        }

    @staticmethod
    def project_statistics(
        db: Session
    ):

        return {
            "active_projects":
                db.query(Project)
                .filter(
                    Project.status == "active"
                )
                .count(),

            "completed_projects":
                db.query(Project)
                .filter(
                    Project.status == "completed"
                )
                .count(),

            "total_projects":
                db.query(Project).count()
        }

    @staticmethod
    def task_statistics(
        db: Session
    ):

        return {
            "todo":
                db.query(Task)
                .filter(
                    Task.status == "todo"
                )
                .count(),

            "in_progress":
                db.query(Task)
                .filter(
                    Task.status == "in_progress"
                )
                .count(),

            "completed":
                db.query(Task)
                .filter(
                    Task.status == "completed"
                )
                .count(),

            "total_tasks":
                db.query(Task).count()
        }

    @staticmethod
    def bug_statistics(
        db: Session
    ):

        return {
            "open":
                db.query(Bug)
                .filter(
                    Bug.status == "open"
                )
                .count(),

            "in_progress":
                db.query(Bug)
                .filter(
                    Bug.status == "in_progress"
                )
                .count(),

            "resolved":
                db.query(Bug)
                .filter(
                    Bug.status == "resolved"
                )
                .count(),

            "closed":
                db.query(Bug)
                .filter(
                    Bug.status == "closed"
                )
                .count(),

            "total_bugs":
                db.query(Bug).count()
        }

    @staticmethod
    def knowledge_statistics(
        db: Session
    ):

        return {
            "draft":
                db.query(Knowledge)
                .filter(
                    Knowledge.status == "draft"
                )
                .count(),

            "published":
                db.query(Knowledge)
                .filter(
                    Knowledge.status == "published"
                )
                .count(),

            "total_knowledge":
                db.query(Knowledge).count()
        }