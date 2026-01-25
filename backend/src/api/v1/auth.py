from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, Any
from src.database import get_session
from src.models import User, UserCreate, UserLogin, UserRead
import hashlib
import uuid

router = APIRouter()

def verify_password(plain_password, hashed_password):
    """Verify a password against a hash"""
    # Create a hash of the plain password and compare
    return get_password_hash(plain_password) == hashed_password

def get_password_hash(password):
    """Hash a password with SHA-256"""
    # Truncate to 72 bytes if needed to avoid bcrypt limitation
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    # Use SHA-256 for password hashing
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@router.post("/signup")
def signup(user: UserCreate, session: Session = Depends(get_session)) -> Dict[str, Any]:
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create new user
    db_user = User(email=user.email, password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Return the required format: {"token": "<jwt>", "user": {"id": string, "email": string}}
    # But without actual token since we're removing auth
    return {
        "token": "",  # Empty token since we're removing auth
        "user": {
            "id": str(db_user.id),
            "email": db_user.email
        }
    }

@router.post("/signin")
def signin(user_credentials: UserLogin, session: Session = Depends(get_session)) -> Dict[str, Any]:
    # Find user by email
    user = session.exec(select(User).where(User.email == user_credentials.email)).first()

    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Return the required format: {"token": "<jwt>", "user": {"id": string, "email": string}}
    # But without actual token since we're removing auth
    return {
        "token": "",  # Empty token since we're removing auth
        "user": {
            "id": str(user.id),
            "email": user.email
        }
    }

@router.post("/signout")
def signout():
    # Simple signout - no tokens to invalidate on the client side
    return {"message": "Signed out successfully"}