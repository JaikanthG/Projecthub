from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models import (
    Project,
    Knowledge,
    Bug,
    Task
)


class SearchRepository:

    @staticmethod
    def global_search(
        keyword: str,
        db: Session
    ):

        knowledge = (
            db.query(Knowledge)
            .filter(
                or_(
                    Knowledge.title.ilike(
                        f"%{keyword}%"
                    ),
                    Knowledge.content.ilike(
                        f"%{keyword}%"
                    ),
                    Knowledge.tags.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

        bugs = (
            db.query(Bug)
            .filter(
                or_(
                    Bug.title.ilike(
                        f"%{keyword}%"
                    ),
                    Bug.description.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

        tasks = (
            db.query(Task)
            .filter(
                or_(
                    Task.title.ilike(
                        f"%{keyword}%"
                    ),
                    Task.description.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

        projects = (
            db.query(Project)
            .filter(
                or_(
                    Project.project_name.ilike(
                        f"%{keyword}%"
                    ),
                    Project.description.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

        return {
            "projects": projects,
            "knowledge": knowledge,
            "bugs": bugs,
            "tasks": tasks
        }

    @staticmethod
    def search_knowledge(
        keyword: str,
        db: Session
    ):

        return (
            db.query(Knowledge)
            .filter(
                or_(
                    Knowledge.title.ilike(
                        f"%{keyword}%"
                    ),
                    Knowledge.content.ilike(
                        f"%{keyword}%"
                    ),
                    Knowledge.tags.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

    @staticmethod
    def search_bugs(
        keyword: str,
        db: Session
    ):

        return (
            db.query(Bug)
            .filter(
                or_(
                    Bug.title.ilike(
                        f"%{keyword}%"
                    ),
                    Bug.description.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

    @staticmethod
    def search_tasks(
        keyword: str,
        db: Session
    ):

        return (
            db.query(Task)
            .filter(
                or_(
                    Task.title.ilike(
                        f"%{keyword}%"
                    ),
                    Task.description.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

    @staticmethod
    def filter_search(
        project_name: str,
        keyword: str,
        db: Session
    ):

        project = (
            db.query(Project)
            .filter(
                Project.project_name.ilike(
                    f"%{project_name}%"
                )
            )
            .first()
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        knowledge = (
            db.query(Knowledge)
            .filter(
                Knowledge.project_id == project.id,
                or_(
                    Knowledge.title.ilike(
                        f"%{keyword}%"
                    ),
                    Knowledge.content.ilike(
                        f"%{keyword}%"
                    ),
                    Knowledge.tags.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

        bugs = (
            db.query(Bug)
            .filter(
                Bug.project_id == project.id,
                or_(
                    Bug.title.ilike(
                        f"%{keyword}%"
                    ),
                    Bug.description.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

        tasks = (
            db.query(Task)
            .filter(
                Task.project_id == project.id,
                or_(
                    Task.title.ilike(
                        f"%{keyword}%"
                    ),
                    Task.description.ilike(
                        f"%{keyword}%"
                    )
                )
            )
            .all()
        )

        return {
            "project": project.project_name,
            "knowledge": knowledge,
            "bugs": bugs,
            "tasks": tasks
        }