import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal, engine
from src.models import Base

# Create a test client
client = TestClient(app)

def setup_module():
    """Set up the test database"""
    Base.metadata.create_all(bind=engine)

def teardown_module():
    """Clean up the test database"""
    Base.metadata.drop_all(bind=engine)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_signup():
    """Test the signup endpoint"""
    response = client.post(
        "/api/v1/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["email"] == "test@example.com"

def test_signin():
    """Test the signin endpoint"""
    response = client.post(
        "/api/v1/signin",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["email"] == "test@example.com"

def test_create_task():
    """Test creating a task"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "owner_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"

def test_get_tasks():
    """Test getting tasks"""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)