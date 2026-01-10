#!/usr/bin/env python3
"""
Simple test to verify that the backend can start without errors
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set the environment file
os.environ.setdefault('ENV_FILE', str(project_root / '.env'))

def test_backend_startup():
    """Test that the backend can be imported and initialized without errors"""
    try:
        # Import the main app
        from backend.src.main import app
        
        # Verify that the app has the expected routes
        assert len(app.routes) > 0, "App should have routes defined"
        
        # Check that the tasks router is included
        route_names = [route.name for route in app.routes]
        assert any('tasks' in name.lower() for name in route_names), "Tasks routes should be included"
        
        print("[OK] Backend startup test passed!")
        print(f"[OK] App has {len(app.routes)} routes")
        print(f"[OK] Available routes: {[route.path for route in app.routes if hasattr(route, 'path')]}")

        return True

    except Exception as e:
        print(f"[ERROR] Backend startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_backend_startup()
    if not success:
        sys.exit(1)