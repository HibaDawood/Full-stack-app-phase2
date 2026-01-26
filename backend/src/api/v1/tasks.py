from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from src.database import get_session
from src.models import Task, TaskCreate, TaskUpdate, TaskRead, User
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[TaskRead])
def get_tasks(user_id: Optional[int] = None, session: Session = Depends(get_session)):
    # If user_id is provided, return only that user's tasks
    # Otherwise, return all tasks (for backward compatibility)
    if user_id:
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
    else:
        tasks = session.exec(select(Task)).all()

    return [
        TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead(**task.model_dump())
        for task in tasks
    ]

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str, session: Session = Depends(get_session)):
    from uuid import UUID
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    task = session.get(Task, task_uuid)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead(**task.model_dump())

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    # Create task without associating to a specific user (no authentication)
    # Get the first user from the database to use as default
    first_user = session.exec(select(User)).first()
    if not first_user:
        # If no users exist, we'll create a default user first
        from hashlib import sha256
        default_email = "default@example.com"
        default_password = sha256("default_password".encode()).hexdigest()
        first_user = User(email=default_email, password=default_password)
        session.add(first_user)
        session.commit()
        session.refresh(first_user)

    # Convert pydantic model to dict and add the user_id
    task_dict = task.model_dump()  # Use model_dump() instead of deprecated dict()
    task_dict['user_id'] = first_user.id

    db_task = Task(**task_dict)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(**db_task.model_dump())

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task_update: TaskUpdate, session: Session = Depends(get_session)):
    from uuid import UUID
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    db_task = session.get(Task, task_uuid)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task fields
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead(**db_task.model_dump())

@router.delete("/{task_id}")
def delete_task(task_id: str, session: Session = Depends(get_session)):
    from uuid import UUID
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    task = session.get(Task, task_uuid)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}