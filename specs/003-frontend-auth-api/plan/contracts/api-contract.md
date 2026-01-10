# API Contract: Frontend UI & Auth Integration

## Authentication Endpoints

### POST /auth/signup
Register a new user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "confirmPassword": "securePassword123"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-01-08T10:00:00.000Z",
    "updated_at": "2026-01-08T10:00:00.000Z"
  },
  "token": "jwt-token-string",
  "expires_at": "2026-01-09T10:00:00.000Z"
}
```

**Response (400):**
```json
{
  "error": "Validation error message"
}
```

**Response (409):**
```json
{
  "error": "User already exists"
}
```

### POST /auth/signin
Login an existing user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-01-08T10:00:00.000Z",
    "updated_at": "2026-01-08T10:00:00.000Z"
  },
  "token": "jwt-token-string",
  "expires_at": "2026-01-09T10:00:00.000Z"
}
```

**Response (400):**
```json
{
  "error": "Invalid credentials"
}
```

### POST /api/auth/logout
Logout the current user

**Response (200):**
```json
{
  "message": "Successfully logged out"
}
```

## Task Management Endpoints

### GET /api/tasks
Retrieve all tasks for the authenticated user

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (200):**
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Task description",
      "status": "pending",
      "user_id": "user-uuid-string",
      "created_at": "2026-01-08T10:00:00.000Z",
      "updated_at": "2026-01-08T10:00:00.000Z"
    }
  ]
}
```

**Response (401):**
```json
{
  "error": "Unauthorized"
}
```

### POST /api/tasks
Create a new task for the authenticated user

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Request:**
```json
{
  "title": "New task title",
  "description": "Task description",
  "status": "pending"
}
```

**Response (201):**
```json
{
  "task": {
    "id": "uuid-string",
    "title": "New task title",
    "description": "Task description",
    "status": "pending",
    "user_id": "user-uuid-string",
    "created_at": "2026-01-08T10:00:00.000Z",
    "updated_at": "2026-01-08T10:00:00.000Z"
  }
}
```

**Response (400):**
```json
{
  "error": "Validation error message"
}
```

**Response (401):**
```json
{
  "error": "Unauthorized"
}
```

### GET /api/tasks/{task_id}
Retrieve a specific task

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (200):**
```json
{
  "task": {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "status": "pending",
    "user_id": "user-uuid-string",
    "created_at": "2026-01-08T10:00:00.000Z",
    "updated_at": "2026-01-08T10:00:00.000Z"
  }
}
```

**Response (401):**
```json
{
  "error": "Unauthorized"
}
```

**Response (404):**
```json
{
  "error": "Task not found"
}
```

### PUT /api/tasks/{task_id}
Update a specific task

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Request:**
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "status": "in-progress"
}
```

**Response (200):**
```json
{
  "task": {
    "id": "uuid-string",
    "title": "Updated task title",
    "description": "Updated task description",
    "status": "in-progress",
    "user_id": "user-uuid-string",
    "created_at": "2026-01-08T10:00:00.000Z",
    "updated_at": "2026-01-08T11:00:00.000Z"
  }
}
```

**Response (400):**
```json
{
  "error": "Validation error message"
}
```

**Response (401):**
```json
{
  "error": "Unauthorized"
}
```

**Response (404):**
```json
{
  "error": "Task not found"
}
```

### DELETE /api/tasks/{task_id}
Delete a specific task

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response (200):**
```json
{
  "message": "Task deleted successfully"
}
```

**Response (401):**
```json
{
  "error": "Unauthorized"
}
```

**Response (404):**
```json
{
  "error": "Task not found"
}
```