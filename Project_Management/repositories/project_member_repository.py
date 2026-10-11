from sqlalchemy.orm import Session

from ..models import (
    User,
    Project,
    ProjectMember
)


class ProjectMemberRepository:

    @staticmethod
    def get_project(
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

    @staticmethod
    def get_user(
        user_id: int,
        db: Session
    ):

        return (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )

    @staticmethod
    def get_member(
        member_id: int,
        db: Session
    ):

        return (
            db.query(ProjectMember)
            .filter(
                ProjectMember.id == member_id
            )
            .first()
        )

    @staticmethod
    def get_project_members(
        project_id: int,
        db: Session
    ):

        return (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id
            )
            .all()
        )

    @staticmethod
    def get_existing_member(
        project_id: int,
        user_id: int,
        db: Session
    ):

        return (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def assign_member(
        member: ProjectMember,
        db: Session
    ):

        db.add(member)
        db.commit()
        db.refresh(member)

        return member

    @staticmethod
    def update_member(
        db: Session
    ):

        db.commit()

    @staticmethod
    def delete_member(
        member: ProjectMember,
        db: Session
    ):

        db.delete(member)
        db.commit()