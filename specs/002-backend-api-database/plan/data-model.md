# Data Model Design: Backend API & Database Layer

**Feature**: Backend API & Database Layer
**Created**: 2026-01-08
**Status**: Completed

## Entity: User

### Fields
- **id** (UUID, Primary Key)
  - Type: `UUID` (from `sqlmodel.sql.sqltypes.GUID`)
  - Constraints: Primary Key, Not Null, Unique
  - Description: Unique identifier for the user
  
- **email** (String)
  - Type: `str`
  - Constraints: Not Null, Unique, Max Length 255
  - Description: User's email address used for identification
  
- **created_at** (DateTime)
  - Type: `datetime`
  - Constraints: Not Null, Default to current timestamp
  - Description: Timestamp when the user account was created
  
- **updated_at** (DateTime)
  - Type: `datetime`
  - Constraints: Not Null, Default to current timestamp
  - Description: Timestamp when the user account was last updated

### Relationships
- **tasks**: One-to-Many relationship with Task entity (User has many Tasks)

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- ID must be a valid UUID

## Entity: Task

### Fields
- **id** (UUID, Primary Key)
  - Type: `UUID` (from `sqlmodel.sql.sqltypes.GUID`)
  - Constraints: Primary Key, Not Null, Unique
  - Description: Unique identifier for the task
  
- **title** (String)
  - Type: `str`
  - Constraints: Not Null, Max Length 255
  - Description: Title or subject of the task
  
- **description** (Text)
  - Type: `str` (optional)
  - Constraints: Nullable
  - Description: Detailed description of the task
  
- **status** (String)
  - Type: `str`
  - Constraints: Not Null, Default "pending", Check constraint for allowed values
  - Allowed Values: "pending", "in-progress", "completed"
  - Description: Current status of the task
  
- **user_id** (UUID, Foreign Key)
  - Type: `UUID` (from `sqlmodel.sql.sqltypes.GUID`)
  - Constraints: Not Null, Foreign Key to User.id
  - Description: Reference to the user who owns this task
  
- **created_at** (DateTime)
  - Type: `datetime`
  - Constraints: Not Null, Default to current timestamp
  - Description: Timestamp when the task was created
  
- **updated_at** (DateTime)
  - Type: `datetime`
  - Constraints: Not Null, Default to current timestamp
  - Description: Timestamp when the task was last updated

### Relationships
- **user**: Many-to-One relationship with User entity (Task belongs to one User)

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

## Database Constraints

### Primary Keys
- Both User and Task entities have UUID primary keys

### Foreign Keys
- Task.user_id references User.id with CASCADE delete behavior

### Indexes
- Index on User.email for efficient lookup
- Index on Task.user_id for efficient filtering by user
- Index on Task.status for efficient status-based queries

## Security Considerations
- All queries involving tasks must filter by user_id to ensure data isolation
- Direct access to tasks should always be validated against the authenticated user
- No direct access to another user's tasks should be possible through any endpoint