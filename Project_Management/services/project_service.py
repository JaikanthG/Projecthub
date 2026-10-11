from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Project

from ..repositories.project_repository import (
    ProjectRepository
)

from ..repositories.activity_repository import (
    ActivityRepository
)

from ..utils.permissions import (
    require_admin
)


class ProjectService:

    # ==========================================================
    # CREATE PROJECT
    # ==========================================================

    @staticmethod
    def create_project(
        project,
        current_user: dict,
        db: Session
    ):

        # ------------------------------------------------------
        # Only Admin can create projects
        # ------------------------------------------------------

        require_admin(
            current_user
        )

        # ------------------------------------------------------
        # Check duplicate project
        # ------------------------------------------------------

        existing_project = (
            ProjectRepository.get_project_by_name(
                project.project_name,
                db
            )
        )

        if existing_project:

            raise HTTPException(
                status_code=400,
                detail="Project already exists."
            )

        # ------------------------------------------------------
        # Create Project object
        # ------------------------------------------------------

        new_project = Project(
            project_name=project.project_name,
            description=project.description,
            technology_stack=project.technology_stack,
            status=project.status,
            created_by=current_user["user_id"]
        )

        # ------------------------------------------------------
        # Save project
        # ------------------------------------------------------

        created_project = (
            ProjectRepository.create_project(
                new_project,
                db
            )
        )

        # ------------------------------------------------------
        # Activity log
        # ------------------------------------------------------

        ActivityRepository.create_activity(
            project_id=created_project.id,
            user_id=current_user["user_id"],
            action="CREATE",
            entity_type="PROJECT",
            entity_id=created_project.id,
            description=(
                f"Created project: "
                f"{created_project.project_name}"
            ),
            db=db
        )

        return created_project


    # ==========================================================
    # GET ALL PROJECTS
    # ==========================================================

    @staticmethod
    def get_all_projects(
        db: Session
    ):

        return (
            ProjectRepository.get_all_projects(
                db
            )
        )


    # ==========================================================
    # GET PROJECT BY ID
    # ==========================================================

    @staticmethod
    def get_project_by_id(
        project_id: int,
        db: Session
    ):

        project = (
            ProjectRepository.get_project_by_id(
                project_id,
                db
            )
        )

        if project is None:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        return project


    # ==========================================================
    # UPDATE PROJECT
    # ==========================================================

    @staticmethod
    def update_project(
        project_id: int,
        updated_project,
        current_user: dict,
        db: Session
    ):

        # ------------------------------------------------------
        # Only Admin can update projects
        # ------------------------------------------------------

        require_admin(
            current_user
        )

        # ------------------------------------------------------
        # Find project
        # ------------------------------------------------------

        project = (
            ProjectRepository.get_project_by_id(
                project_id,
                db
            )
        )

        if project is None:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        # ------------------------------------------------------
        # Check duplicate project name
        # ------------------------------------------------------

        duplicate_project = (
            ProjectRepository.get_project_by_name(
                updated_project.project_name,
                db
            )
        )

        if (
            duplicate_project
            and duplicate_project.id != project_id
        ):

            raise HTTPException(
                status_code=400,
                detail="Project already exists."
            )

        # ------------------------------------------------------
        # Update fields
        # ------------------------------------------------------

        project.project_name = (
            updated_project.project_name
        )

        project.description = (
            updated_project.description
        )

        project.technology_stack = (
            updated_project.technology_stack
        )

        project.status = (
            updated_project.status
        )

        # ------------------------------------------------------
        # Save changes
        # ------------------------------------------------------

        updated_project_result = (
            ProjectRepository.update_project(
                db
            )
        )

        # ------------------------------------------------------
        # Activity log
        # ------------------------------------------------------

        ActivityRepository.create_activity(
            project_id=project.id,
            user_id=current_user["user_id"],
            action="UPDATE",
            entity_type="PROJECT",
            entity_id=project.id,
            description=(
                f"Updated project: "
                f"{project.project_name}"
            ),
            db=db
        )

        return project


    # ==========================================================
    # DELETE PROJECT
    # ==========================================================

    @staticmethod
    def delete_project(
        project_id: int,
        current_user: dict,
        db: Session
    ):

        # ------------------------------------------------------
        # Only Admin can delete projects
        # ------------------------------------------------------

        require_admin(
            current_user
        )

        # ------------------------------------------------------
        # Find project
        # ------------------------------------------------------

        project = (
            ProjectRepository.get_project_by_id(
                project_id,
                db
            )
        )

        if project is None:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        # ------------------------------------------------------
        # Activity log BEFORE deletion
        # ------------------------------------------------------

        ActivityRepository.create_activity(
            project_id=project.id,
            user_id=current_user["user_id"],
            action="DELETE",
            entity_type="PROJECT",
            entity_id=project.id,
            description=(
                f"Deleted project: "
                f"{project.project_name}"
            ),
            db=db
        )

        # ------------------------------------------------------
        # Delete project
        # ------------------------------------------------------

        ProjectRepository.delete_project(
            project,
            db
        )

        return {
            "message": "Project deleted successfully."
        }