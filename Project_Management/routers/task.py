# routers/task.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..schemas import (
    CreateTask,
    UpdateTask,
    AssignTask,
    UpdateTaskStatus
)

from ..services.task_service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Task Management"]
)


# ==========================================
# Create Task
# ==========================================

@router.post("/")
def create_task(
    task: CreateTask,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    created_task = TaskService.create_task(
        task,
        current_user,
        db
    )

    return {
        "message": "Task created successfully.",
        "data": created_task
    }


# ==========================================
# Get All Tasks
# ==========================================

@router.get("/")
def get_all_tasks(
    project_id: int = Query(
        ...,
        description="Current project ID"
    ),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    tasks = TaskService.get_all_tasks(
        project_id,
        db
    )

    return {
        "count": len(tasks),
        "data": tasks
    }


# ==========================================
# Get Task By ID
# ==========================================

@router.get("/{task_id}")
def get_task_by_id(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return TaskService.get_task_by_id(
        task_id,
        db
    )


# ==========================================
# Update Task
# ==========================================

@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: UpdateTask,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    updated_task = TaskService.update_task(
        task_id,
        task,
        current_user,
        db
    )

    return {
        "message": "Task updated successfully.",
        "data": updated_task
    }


# ==========================================
# Delete Task
# ==========================================

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return TaskService.delete_task(
        task_id,
        current_user,
        db
    )


# ==========================================
# Assign Task
# ==========================================

@router.put("/{task_id}/assign")
def assign_task(
    task_id: int,
    assign: AssignTask,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    assigned_task = TaskService.assign_task(
        task_id,
        assign,
        current_user,
        db
    )

    return {
        "message": "Task assigned successfully.",
        "data": assigned_task
    }


# ==========================================
# Update Task Status
# ==========================================

@router.put("/{task_id}/status")
def update_task_status(
    task_id: int,
    status: UpdateTaskStatus,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    updated_task = TaskService.update_status(
        task_id,
        status,
        current_user,
        db
    )

    return {
        "message": "Task status updated successfully.",
        "data": updated_task
    }