import os
import sys
# Set environment variables BEFORE importing any modules that use settings
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['BETTER_AUTH_SECRET'] = 'KQbdC62kWWhTNKTQLjsV5BjqAmfAXnDU'

sys.path.append('./backend')

from fastapi import FastAPI, Depends
from sqlmodel import Session
from backend.src.api.deps import get_session
from backend.src.models.user import User
from backend.src.schemas.auth import UserCreate, AuthResponse, UserResponse
from backend.src.services.auth_service import create_user

app = FastAPI(title="Test API")

@app.post("/auth/signup", response_model=AuthResponse)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    db_user = create_user(session=session, user_create=user_create)

    # Create a simple token (just the user ID) instead of JWT
    simple_token = str(db_user.id)

    user_response = UserResponse(
        id=db_user.id,
        email=db_user.email,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    )
    return AuthResponse(
        token=simple_token,
        user=user_response
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)