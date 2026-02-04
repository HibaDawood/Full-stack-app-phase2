from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

# Pure Pydantic models to avoid SQLModel compatibility issues
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserRead(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"  # Changed from completed to status to match DB

class TaskCreate(TaskBase):
    user_id: Optional[UUID] = None  # Allow user_id to be optional when creating

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # Changed from completed to status

class TaskRead(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# For database operations, we'll use raw SQLAlchemy models
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import text
import uuid

Base = declarative_base()

class UserOrm(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # This will store the hashed password
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class TaskOrm(Base):
    __tablename__ = "task"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String, nullable=True)
    status = Column(String, default="pending")  # Changed from completed to status to match DB
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))  # Note: referencing the table name
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())