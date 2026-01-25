from fastapi import Depends
from sqlmodel import Session
from ..database import engine
from ..models.user import User


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session