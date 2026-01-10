# Data Model: Secure Todo Full-Stack Web Application

## Overview
This document defines the data models for the secure todo application, including entities, relationships, and validation rules.

## Entities

### User
Represents a registered user of the application

**Fields:**
- id (UUID, primary key): Unique identifier for the user
- email (String, unique, required): Email address for login
- hashed_password (String, required): Hashed password for authentication
- created_at (DateTime, required): Timestamp when the user was created
- updated_at (DateTime, required): Timestamp when the user was last updated
- is_active (Boolean, default: True): Whether the account is active

**Validation Rules:**
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum security requirements (handled by Better Auth)

**Relationships:**
- One-to-many with Task (user has many tasks)

### Task
Represents a personal task owned by a specific user

**Fields:**
- id (UUID, primary key): Unique identifier for the task
- title (String, required): Brief title of the task
- description (Text, optional): Detailed description of the task
- is_completed (Boolean, default: False): Whether the task is completed
- created_at (DateTime, required): Timestamp when the task was created
- updated_at (DateTime, required): Timestamp when the task was last updated
- owner_id (UUID, foreign key): Reference to the user who owns this task

**Validation Rules:**
- Title must not be empty
- Owner_id must reference an existing user
- Only the owner can modify or delete the task

**Relationships:**
- Many-to-one with User (task belongs to one user)

## State Transitions

### Task State Transitions
- Created → Active (default state when created)
- Active ↔ Completed (toggled by user)
- Any state → Deleted (removed from system)

## Indexes
- User.email: For efficient lookup during authentication
- Task.owner_id: For efficient querying of user's tasks
- Task.created_at: For sorting and filtering by creation date