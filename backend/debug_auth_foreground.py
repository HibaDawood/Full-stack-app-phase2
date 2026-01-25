import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from src.database import engine
from src.models.user import User
from src.schemas.auth import UserCreate
from src.services.auth_service import create_user, create_access_token
from src.config import settings

app = FastAPI()

security = HTTPBearer()

@app.post("/auth/signup")
def signup(user_create: UserCreate):
    try:
        print("Signup endpoint called")
        
        # Create a temporary session for testing
        with Session(engine) as session:
            print("Creating user...")
            db_user = create_user(session=session, user_create=user_create)
            
            print("Creating access token...")
            access_token = create_access_token(
                data={"sub": str(db_user.id), "email": db_user.email}
            )
            
            print("Returning response...")
            return {
                "token": access_token,
                "user": {
                    "id": str(db_user.id),
                    "email": db_user.email,
                    "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
                    "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None
                }
            }
    except Exception as e:
        print(f"Error in signup: {e}")
        import traceback
        traceback.print_exc()
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")