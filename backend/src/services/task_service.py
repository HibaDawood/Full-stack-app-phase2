from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
from ..utils.exceptions import TaskNotFoundException, UnauthorizedAccessException
import uuid
from datetime import datetime


def create_task(*, session: Session, task_create: TaskCreate, user_id: uuid.UUID) -> Task:
    """
    Create a new task for the authenticated user
    """
    # Create a new Task instance with the provided data
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        status=task_create.status,
        user_id=user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_tasks_by_user(*, session: Session, user_id: uuid.UUID) -> List[Task]:
    """
    Get all tasks for the authenticated user
    """
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


def get_task_by_id_and_user(*, session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
    """
    Get a specific task by ID for the authenticated user
    """
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    return task


def update_task_by_id_and_user(
    *, session: Session, task_id: uuid.UUID, task_update: TaskUpdate, user_id: uuid.UUID
) -> Task:
    """
    Update a specific task by ID for the authenticated user
    """
    db_task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not db_task:
        raise TaskNotFoundException(str(task_id))

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task_by_id_and_user(*, session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """
    Delete a specific task by ID for the authenticated user
    """
    db_task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not db_task:
        raise TaskNotFoundException(str(task_id))

    session.delete(db_task)
    session.commit()
    return True