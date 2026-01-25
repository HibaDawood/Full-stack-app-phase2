from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from src.database import engine
from src.models.user import User
from src.models.task import TaskCreate
from src.services.task_service import create_task
from src.utils.auth import get_current_user
from src.config import settings

app = FastAPI()

security = HTTPBearer()

@app.post("/debug/tasks")
def debug_create_task(task: TaskCreate, current_user = Depends(get_current_user)):
    """Debug endpoint to test task creation"""
    print(f"Current user: {current_user}")
    print(f"Task data: {task}")
    
    with Session(engine) as session:
        db_task = create_task(session=session, task_create=task, user_id=current_user.id)
        print(f"Created task: {db_task}")
        return db_task

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")