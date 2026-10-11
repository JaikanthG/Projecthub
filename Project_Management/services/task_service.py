from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import (
    Task,
    Project,
    User
)

from ..repositories.task_repository import (
    TaskRepository
)

from ..repositories.activity_repository import (
    ActivityRepository
)

from ..repositories.notification_repository import (
    NotificationRepository
)

from ..utils.permissions import (
    require_admin,
    require_contributor_or_admin
)


class TaskService:

    # ==========================================
    # Create Task
    # ==========================================

    @staticmethod
    def create_task(
        task,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Check Project
        # ==========================================

        project = db.query(Project).filter(
            Project.id == task.project_id
        ).first()

        if project is None:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        # ==========================================
        # RBAC
        #
        # Admin                -> Allowed
        # Employee + Contributor -> Allowed
        # Employee + Member      -> Denied
        # ==========================================

        require_contributor_or_admin(
            task.project_id,
            current_user,
            db
        )

        # ==========================================
        # Check Duplicate Task
        # ==========================================

        existing_task = (
            TaskRepository.get_task_by_title(
                task.title,
                db
            )
        )

        if existing_task:

            raise HTTPException(
                status_code=400,
                detail="Task title already exists."
            )

        # ==========================================
        # Create Task
        # ==========================================

        new_task = Task(
            project_id=task.project_id,
            title=task.title,
            description=task.description,
            priority=task.priority.lower(),
            status="todo",
            due_date=datetime.fromisoformat(
                task.due_date
            ),
            created_by=current_user["user_id"]
        )

        created_task = (
            TaskRepository.create_task(
                new_task,
                db
            )
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=created_task.project_id,
            user_id=current_user["user_id"],
            action="CREATE",
            entity_type="TASK",
            entity_id=created_task.id,
            description=(
                f"Created task: "
                f"{created_task.title}"
            ),
            db=db
        )

        return created_task


    # ==========================================
    # Get All Tasks
    # ==========================================

    @staticmethod
    def get_all_tasks(
        project_id: int,
        db: Session
    ):

        return TaskRepository.get_all_tasks(
            project_id,
            db
        )


    # ==========================================
    # Get Task By ID
    # ==========================================

    @staticmethod
    def get_task_by_id(
        task_id: int,
        db: Session
    ):

        task = TaskRepository.get_task_by_id(
            task_id,
            db
        )

        if task is None:

            raise HTTPException(
                status_code=404,
                detail="Task not found."
            )

        return task


    # ==========================================
    # Update Task
    # ==========================================

    @staticmethod
    def update_task(
        task_id: int,
        updated_task,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Get Task
        # ==========================================

        task = TaskRepository.get_task_by_id(
            task_id,
            db
        )

        if task is None:

            raise HTTPException(
                status_code=404,
                detail="Task not found."
            )

        # ==========================================
        # RBAC
        #
        # Admin                -> Allowed
        # Employee + Contributor -> Allowed
        # Employee + Member      -> Denied
        # ==========================================

        require_contributor_or_admin(
            task.project_id,
            current_user,
            db
        )

        # ==========================================
        # Update Task
        # ==========================================

        task.title = updated_task.title

        task.description = (
            updated_task.description
        )

        task.priority = (
            updated_task.priority.lower()
        )

        task.status = (
            updated_task.status.lower()
        )

        task.due_date = datetime.fromisoformat(
            updated_task.due_date
        )

        TaskRepository.update_task(
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=task.project_id,
            user_id=current_user["user_id"],
            action="UPDATE",
            entity_type="TASK",
            entity_id=task.id,
            description=(
                f"Updated task: "
                f"{task.title}"
            ),
            db=db
        )

        return task


    # ==========================================
    # Delete Task
    # ==========================================

    @staticmethod
    def delete_task(
        task_id: int,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Get Task
        # ==========================================

        task = TaskRepository.get_task_by_id(
            task_id,
            db
        )

        if task is None:

            raise HTTPException(
                status_code=404,
                detail="Task not found."
            )

        # ==========================================
        # Only Admin Can Delete
        # ==========================================

        require_admin(
            current_user
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=task.project_id,
            user_id=current_user["user_id"],
            action="DELETE",
            entity_type="TASK",
            entity_id=task.id,
            description=(
                f"Deleted task: "
                f"{task.title}"
            ),
            db=db
        )

        # ==========================================
        # Delete Task
        # ==========================================

        TaskRepository.delete_task(
            task,
            db
        )

        return {
            "message": "Task deleted successfully."
        }


    # ==========================================
    # Assign Task
    # ==========================================

    @staticmethod
    def assign_task(
        task_id: int,
        assign,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Only Admin Can Assign
        # ==========================================

        require_admin(
            current_user
        )

        # ==========================================
        # Get Task
        # ==========================================

        task = TaskRepository.get_task_by_id(
            task_id,
            db
        )

        if task is None:

            raise HTTPException(
                status_code=404,
                detail="Task not found."
            )

        # ==========================================
        # Check Assigned User
        # ==========================================

        user = db.query(User).filter(
            User.id == assign.assigned_to
        ).first()

        if user is None:

            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        # ==========================================
        # Assign Task
        # ==========================================

        task.assigned_to = (
            assign.assigned_to
        )

        TaskRepository.update_task(
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=task.project_id,
            user_id=current_user["user_id"],
            action="ASSIGN",
            entity_type="TASK",
            entity_id=task.id,
            description=(
                f"Assigned task "
                f"'{task.title}' "
                f"to user {user.username}"
            ),
            db=db
        )

        # ==========================================
        # Notification
        # ==========================================

        NotificationRepository.create_notification(
            user_id=assign.assigned_to,
            project_id=task.project_id,
            title="Task Assigned",
            message=(
                f"You have been assigned task "
                f"'{task.title}'."
            ),
            notification_type="TASK_ASSIGNMENT",
            db=db
        )

        return task


    # ==========================================
    # Update Task Status
    # ==========================================

    @staticmethod
    def update_status(
        task_id: int,
        status,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Get Task
        # ==========================================

        task = TaskRepository.get_task_by_id(
            task_id,
            db
        )

        if task is None:

            raise HTTPException(
                status_code=404,
                detail="Task not found."
            )

        # ==========================================
        # RBAC
        #
        # Admin                -> Allowed
        # Employee + Contributor -> Allowed
        # Employee + Member      -> Denied
        # ==========================================

        require_contributor_or_admin(
            task.project_id,
            current_user,
            db
        )

        # ==========================================
        # Store Old Status
        # ==========================================

        old_status = task.status

        # ==========================================
        # Update Status
        # ==========================================

        task.status = status.status.lower()

        TaskRepository.update_task(
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=task.project_id,
            user_id=current_user["user_id"],
            action="STATUS_CHANGE",
            entity_type="TASK",
            entity_id=task.id,
            description=(
                f"Changed task "
                f"'{task.title}' status "
                f"from '{old_status}' "
                f"to '{task.status}'"
            ),
            db=db
        )

        return task