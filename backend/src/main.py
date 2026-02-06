from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routers
from src.api.v1.auth import router as auth_router
from src.api.v1.tasks import router as tasks_router
from src.api.v1.health import router as health_router
from src.api.v1.chat import router as chat_router  # Import the chat router
from src.database import create_tables

app = FastAPI(
    title="Todo API",
    description="Backend API for managing user tasks without token authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080", "http://127.0.0.1:8080"],  # Allow Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])  # Changed from "/api/v1" to "/api/v1/tasks"
app.include_router(health_router, tags=["health"])
app.include_router(chat_router)  # Include the chat router

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}