from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from src.database import get_session
from src.models import TaskOrm as Task, UserOrm as User, TaskCreate, TaskUpdate, TaskRead, UserCreate
from uuid import UUID
import hashlib

router = APIRouter()

@router.get("/", response_model=List[TaskRead])
def get_tasks(user_id: str = None, session: Session = Depends(get_session)):
    # If user_id is provided, return only that user's tasks
    # Otherwise, return all tasks (for backward compatibility)
    try:
        if user_id:
            uuid_user_id = UUID(user_id)
            tasks = session.query(Task).filter(Task.user_id == uuid_user_id).all()
        else:
            tasks = session.query(Task).all()

        return [TaskRead.from_orm(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tasks: {str(e)}")

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str, session: Session = Depends(get_session)):
    try:
        uuid_task_id = UUID(task_id)
        task = session.query(Task).filter(Task.id == uuid_task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskRead.from_orm(task)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    try:
        # Create task without associating to a specific user (no authentication)
        # Get the first user from the database to use as default
        first_user = session.query(User).first()
        if not first_user:
            # If no users exist, we'll create a default user first
            default_email = "default@example.com"
            default_password = hashlib.sha256("default_password".encode()).hexdigest()
            first_user = User(email=default_email, password=default_password)
            session.add(first_user)
            session.commit()
            session.refresh(first_user)

        # Create the task object
        db_task = Task(
            title=task.title,
            description=task.description,
            status=task.status,
            user_id=first_user.id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return TaskRead.from_orm(db_task)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task_update: TaskUpdate, session: Session = Depends(get_session)):
    try:
        uuid_task_id = UUID(task_id)
        db_task = session.query(Task).filter(Task.id == uuid_task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update task fields
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return TaskRead.from_orm(db_task)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

@router.delete("/{task_id}")
def delete_task(task_id: str, session: Session = Depends(get_session)):
    try:
        uuid_task_id = UUID(task_id)
        task = session.query(Task).filter(Task.id == uuid_task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")