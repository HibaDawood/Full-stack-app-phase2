from src.services.auth_service import create_access_token
from src.config import settings

# Test JWT creation
try:
    token = create_access_token(data={"sub": "test-user-id", "email": "test@example.com"})
    print("JWT creation successful!")
    print(f"Token: {token}")
except Exception as e:
    print(f"JWT creation failed: {e}")
    import traceback
    traceback.print_exc()