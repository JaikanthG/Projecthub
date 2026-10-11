from sqlalchemy.orm import Session

from ..models import Task


class TaskRepository:

    # ==========================================
    # Get All Tasks For Current Project
    # ==========================================

    @staticmethod
    def get_all_tasks(
        project_id: int,
        db: Session
    ):

        return (
            db.query(Task)
            .filter(
                Task.project_id == project_id
            )
            .all()
        )


    # ==========================================
    # Get Task By ID
    # ==========================================

    @staticmethod
    def get_task_by_id(
        task_id: int,
        db: Session
    ):

        return (
            db.query(Task)
            .filter(
                Task.id == task_id
            )
            .first()
        )


    # ==========================================
    # Get Task By Title
    # ==========================================

    @staticmethod
    def get_task_by_title(
        title: str,
        db: Session
    ):

        return (
            db.query(Task)
            .filter(
                Task.title == title
            )
            .first()
        )


    # ==========================================
    # Create Task
    # ==========================================

    @staticmethod
    def create_task(
        task: Task,
        db: Session
    ):

        db.add(task)
        db.commit()
        db.refresh(task)

        return task


    # ==========================================
    # Update Task
    # ==========================================

    @staticmethod
    def update_task(
        db: Session
    ):

        db.commit()


    # ==========================================
    # Delete Task
    # ==========================================

    @staticmethod
    def delete_task(
        task: Task,
        db: Session
    ):

        db.delete(task)
        db.commit()