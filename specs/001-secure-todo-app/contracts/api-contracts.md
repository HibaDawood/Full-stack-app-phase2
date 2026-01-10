# API Contracts: Secure Todo Full-Stack Web Application

## Overview
This document defines the REST API contracts for the secure todo application, specifying endpoints, request/response formats, and authentication requirements.

## Authentication
All endpoints except authentication endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Base URL
```
https://api.example.com/v1
```

## Common Response Format
Successful responses follow this pattern:
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

Error responses follow this pattern:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## Endpoints

### Authentication Endpoints

#### POST /auth/register
Register a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "confirm_password": "securePassword123"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid-string",
      "email": "user@example.com",
      "created_at": "2023-01-01T00:00:00Z"
    },
    "access_token": "jwt-token-string",
    "token_type": "bearer"
  }
}
```

**Validation:**
- Email must be valid format
- Password must meet security requirements
- Passwords must match

#### POST /auth/login
Authenticate user and return JWT token

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid-string",
      "email": "user@example.com",
      "created_at": "2023-01-01T00:00:00Z"
    },
    "access_token": "jwt-token-string",
    "token_type": "bearer"
  }
}
```

**Validation:**
- Email must exist
- Password must match stored hash

#### POST /auth/logout
Invalidate the current session (stateless - client handles token removal)

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

### Task Management Endpoints

#### GET /tasks
Retrieve all tasks for the authenticated user

**Query Parameters:**
- `completed` (optional, boolean): Filter by completion status
- `limit` (optional, integer): Max number of results (default: 50, max: 100)
- `offset` (optional, integer): Offset for pagination (default: 0)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "uuid-string",
        "title": "Task title",
        "description": "Task description",
        "is_completed": false,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "total": 10,
      "limit": 50,
      "offset": 0
    }
  }
}
```

#### POST /tasks
Create a new task for the authenticated user

**Request Body:**
```json
{
  "title": "New task title",
  "description": "Detailed description of the task"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "uuid-string",
      "title": "New task title",
      "description": "Detailed description of the task",
      "is_completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "owner_id": "user-uuid-string"
    }
  }
}
```

**Validation:**
- Title is required and not empty
- Description, if provided, must be under 1000 characters

#### GET /tasks/{task_id}
Retrieve a specific task by ID

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Task description",
      "is_completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "owner_id": "user-uuid-string"
    }
  }
}
```

**Error Responses:**
- 404: Task not found
- 403: User does not own this task

#### PUT /tasks/{task_id}
Update an existing task

**Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "is_completed": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "uuid-string",
      "title": "Updated task title",
      "description": "Updated description",
      "is_completed": true,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-02T00:00:00Z",
      "owner_id": "user-uuid-string"
    }
  }
}
```

**Validation:**
- Task must exist and be owned by the authenticated user
- At least one field must be provided for update

#### DELETE /tasks/{task_id}
Delete a specific task

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Error Responses:**
- 404: Task not found
- 403: User does not own this task

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| AUTH_001 | 401 | Invalid or expired token |
| AUTH_002 | 401 | Invalid credentials |
| AUTH_003 | 403 | Insufficient permissions |
| VALIDATION_001 | 422 | Validation error |
| RESOURCE_001 | 404 | Resource not found |
| SERVER_001 | 500 | Internal server error |