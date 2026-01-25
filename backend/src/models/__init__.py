from .user import User, UserRead
from .task import Task, TaskRead, TaskCreate, TaskUpdate

# Define additional models that are needed
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
import uuid

class UserCreate(SQLModel):
    email: str
    password: str

class UserLogin(SQLModel):
    email: str
    password: str

class UserPublic(SQLModel):
    id: uuid.UUID
    email: str
    created_at: datetime

class TaskPublic(SQLModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    status: str
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

__all__ = ["User", "Task", "UserRead", "TaskRead", "TaskCreate", "TaskUpdate", "UserCreate", "UserLogin", "UserPublic", "TaskPublic"]