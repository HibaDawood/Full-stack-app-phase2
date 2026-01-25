from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str  # This will store the hashed password
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(SQLModel):
    email: str
    password: str

class UserLogin(SQLModel):
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    email: str
    created_at: datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = Field(default="pending")  # Changed from completed to status to match DB
    user_id: int = Field(foreign_key="user.id")  # Note: SQLModel uses plural table names by default
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    status: str = Field(default="pending")  # Changed from completed to status
    user_id: Optional[int] = None  # Allow user_id to be optional when creating

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # Changed from completed to status

class TaskRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str  # Changed from completed to status
    user_id: int
    created_at: datetime
    updated_at: datetime