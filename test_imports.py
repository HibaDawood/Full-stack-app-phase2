try:
    from backend.src.api.v1 import auth
    print("Auth module imported successfully")
except Exception as e:
    print(f"Error importing auth module: {e}")
    import traceback
    traceback.print_exc()

try:
    from backend.src.api.v1 import tasks
    print("Tasks module imported successfully")
except Exception as e:
    print(f"Error importing tasks module: {e}")
    import traceback
    traceback.print_exc()