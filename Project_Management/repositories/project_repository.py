from sqlalchemy.orm import Session

from ..models import Project


class ProjectRepository:

    # ==========================================================
    # GET ALL PROJECTS
    # ==========================================================

    @staticmethod
    def get_all_projects(
        db: Session
    ):
        return db.query(Project).all()


    # ==========================================================
    # GET PROJECT BY ID
    # ==========================================================

    @staticmethod
    def get_project_by_id(
        project_id: int,
        db: Session
    ):
        return (
            db.query(Project)
            .filter(
                Project.id == project_id
            )
            .first()
        )


    # ==========================================================
    # GET PROJECT BY NAME
    # ==========================================================

    @staticmethod
    def get_project_by_name(
        project_name: str,
        db: Session
    ):
        return (
            db.query(Project)
            .filter(
                Project.project_name == project_name
            )
            .first()
        )


    # ==========================================================
    # CREATE PROJECT
    # ==========================================================

    @staticmethod
    def create_project(
        project: Project,
        db: Session
    ):
        db.add(project)

        db.commit()

        db.refresh(project)

        return project


    # ==========================================================
    # UPDATE PROJECT
    # ==========================================================

    @staticmethod
    def update_project(
        db: Session
    ):
        db.commit()


    # ==========================================================
    # DELETE PROJECT
    # ==========================================================

    @staticmethod
    def delete_project(
        project: Project,
        db: Session
    ):
        db.delete(project)

        db.commit()