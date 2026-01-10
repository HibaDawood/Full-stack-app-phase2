# Research Findings: Backend API & Database Layer

**Feature**: Backend API & Database Layer
**Created**: 2026-01-08
**Status**: Completed

## R1: JWT Token Structure

### Decision
JWT tokens from Better Auth contain user information in the payload with standard claims plus custom user properties.

### Rationale
Understanding the JWT structure is essential for extracting user ID and other claims needed for authentication and authorization.

### Details
- Standard claims: `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, `jti`
- Better Auth specific claims: `userId`, `email`, `role` (if applicable)
- User ID is available in the `sub` claim or `userId` claim depending on Better Auth configuration
- Token verification requires the `BETTER_AUTH_SECRET` environment variable

### Implementation Notes
- Use `jose` library to decode and verify JWT tokens
- Extract user ID from the `sub` claim in the token payload
- Verify token signature using the `BETTER_AUTH_SECRET`

## R2: Neon PostgreSQL Connection

### Decision
Use standard PostgreSQL connection string format with Neon-specific parameters for serverless connection.

### Rationale
Neon Serverless PostgreSQL has specific connection requirements that differ slightly from traditional PostgreSQL.

### Details
- Connection string format: `postgresql://username:password@ep-xxxx.us-east-1.aws.neon.tech/dbname?sslmode=require`
- Need to install `psycopg2-binary` or `asyncpg` as the PostgreSQL adapter
- Connection pooling is handled automatically by Neon for serverless instances
- Environment variable: `NEON_DATABASE_URL`

### Implementation Notes
- Use SQLModel's create_engine with the Neon connection string
- Configure connection pooling parameters appropriately for serverless
- Handle potential connection timeouts gracefully

## R3: SQLModel Best Practices

### Decision
Implement user-task relationship with proper foreign keys and constraints using SQLModel's relationship features.

### Rationale
Proper data modeling ensures data integrity and efficient queries while enforcing user data isolation.

### Details
- Use UUID for primary keys to ensure global uniqueness
- Implement foreign key relationship between Task and User
- Use cascade options appropriately (e.g., restrict task deletion if user is deleted)
- Add indexes on frequently queried fields like user_id
- Implement proper validation at the model level

### Implementation Notes
- Define User model with proper fields and constraints
- Define Task model with foreign key reference to User
- Use SQLModel's relationship() function for associations
- Add proper indexes for performance

## R4: FastAPI Security Patterns

### Decision
Use FastAPI dependencies with HTTPBearer for JWT token validation and user extraction.

### Rationale
FastAPI's dependency injection system provides a clean way to enforce authentication across endpoints.

### Details
- Create a security dependency that validates JWT tokens
- Extract user information from the token for use in endpoints
- Return 401 Unauthorized for invalid or missing tokens
- Use HTTPBearer for token extraction from Authorization header

### Implementation Notes
- Create a get_current_user dependency function
- Apply the dependency to all protected endpoints
- Handle token expiration and invalid token scenarios
- Cache validated tokens if needed for performance