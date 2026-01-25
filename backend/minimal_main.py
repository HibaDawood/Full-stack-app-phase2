from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.tasks import router as tasks_router
from src.api.v1.auth import router as auth_router
from src.database import create_tables
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Todo API",
    description="Backend API for managing user tasks with simple token authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_router)  # No prefix needed since routes are already prefixed
app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

# Add exception handler to catch errors
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print(f"Global exception: {exc}")
    import traceback
    traceback.print_exc()
    return {"detail": "Internal Server Error"}