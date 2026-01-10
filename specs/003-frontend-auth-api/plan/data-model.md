# Data Model Design: Frontend UI & Auth Integration

**Feature**: Frontend UI & Auth Integration
**Created**: 2026-01-08
**Status**: Completed

## Entity: User (from backend)

### Fields
- **id** (string)
  - Type: `string` (UUID format)
  - Description: Unique identifier for the user
  
- **email** (string)
  - Type: `string`
  - Description: User's email address used for identification
  
- **created_at** (string)
  - Type: `string` (ISO date format)
  - Description: Timestamp when the user account was created
  
- **updated_at** (string)
  - Type: `string` (ISO date format)
  - Description: Timestamp when the user account was last updated

### Validation Rules
- Email must be a valid email format
- ID must be a valid UUID format

## Entity: Task (from backend)

### Fields
- **id** (string)
  - Type: `string` (UUID format)
  - Description: Unique identifier for the task
  
- **title** (string)
  - Type: `string`
  - Constraints: Required, max length 255 characters
  - Description: Title or subject of the task
  
- **description** (string)
  - Type: `string` (optional)
  - Description: Detailed description of the task
  
- **status** (string)
  - Type: `string`
  - Allowed Values: "pending", "in-progress", "completed"
  - Description: Current status of the task
  
- **user_id** (string)
  - Type: `string` (UUID format)
  - Description: Reference to the user who owns this task
  
- **created_at** (string)
  - Type: `string` (ISO date format)
  - Description: Timestamp when the task was created
  
- **updated_at** (string)
  - Type: `string` (ISO date format)
  - Description: Timestamp when the task was last updated

### Validation Rules
- Title is required and must not exceed 255 characters
- Status must be one of the allowed values: "pending", "in-progress", "completed"
- user_id must reference an existing user
- A task can only be accessed by its owner (user_id matches authenticated user)

## State Transitions (if applicable)

### Task Status Transitions
- **Initial State**: "pending"
- **Transitions**:
  - "pending" → "in-progress" (when user starts working on task)
  - "in-progress" → "pending" (when user pauses task)
  - "in-progress" → "completed" (when user finishes task)
  - "completed" → "pending" (when user reopens task)

## Frontend-Specific Models

### API Response Models

#### AuthResponse
- **user**: User object (as defined above)
- **token**: string (JWT token)
- **expires_at**: string (ISO date format)

#### TaskListResponse
- **tasks**: Array of Task objects (as defined above)

#### TaskResponse
- **task**: Task object (as defined above)

### Form Models

#### SignUpForm
- **email**: string (required, valid email format)
- **password**: string (required, min length 8)
- **confirmPassword**: string (required, must match password)

#### SignInForm
- **email**: string (required, valid email format)
- **password**: string (required)

#### TaskForm
- **title**: string (required, max length 255)
- **description**: string (optional)
- **status**: string (optional, default "pending")

## Frontend State Models

### AuthState
- **user**: User object or null
- **isLoading**: boolean
- **error**: string or null
- **isAuthenticated**: boolean

### TaskState
- **tasks**: Array of Task objects
- **selectedTask**: Task object or null
- **isLoading**: boolean
- **error**: string or null
- **isCreating**: boolean
- **isUpdating**: boolean
- **isDeleting**: boolean

## Security Considerations
- All API requests must include JWT token in Authorization header
- Direct access to tasks should always be validated against the authenticated user
- No direct access to another user's tasks should be possible through any frontend component
- Sensitive data should not be stored in client-side storage without proper encryption