from datetime import datetime, timedelta
from src.config import settings

# Test JWT creation and verification
try:
    # Create a test token
    data = {"sub": "test-user-id", "email": "test@example.com"}
    expire = datetime.utcnow() + timedelta(days=7)
    data.update({"exp": expire})
    
    token = jwt.encode(data, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    print(f"Created token: {token}")
    
    # Decode the token
    decoded = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
    print(f"Decoded token: {decoded}")
    
    print("JWT encoding/decoding works correctly!")
    
except Exception as e:
    print(f"JWT test failed: {e}")
    import traceback
    traceback.print_exc()