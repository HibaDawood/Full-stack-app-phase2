from sqlmodel import Session, select
import bcrypt
from datetime import datetime
from typing import Optional
import uuid
from ..models.user import User
from ..schemas.auth import UserCreate, UserLogin


def hash_password(password: str) -> str:
    """Hash a password using bcrypt, ensuring it's not longer than 72 bytes"""
    # Truncate password to 72 bytes if necessary (bcrypt limitation)
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')

    # Convert password to bytes and hash it
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    pwd_bytes = plain_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user or not verify_password(password, user.password):
        return None

    return user


def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password"""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise ValueError("User with this email already exists")

    # Hash the password
    hashed_password = hash_password(user_create.password)

    db_user = User(email=user_create.email, password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user