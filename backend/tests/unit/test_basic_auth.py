import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.config import settings

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API"}

def test_protected_endpoint_without_auth():
    """Test that protected endpoints return 401 without authentication"""
    response = client.get("/api/v1/tasks")
    # This should return 401 or 403 since no authentication is provided
    assert response.status_code in [401, 403]