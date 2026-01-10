---
id: 001
title: Update Project Constitution
stage: constitution
date: 2026-01-08
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
 - .specify/templates/adr-template.md
 - .specify/templates/phr-template.prompt.md
 - README.md
tests:
 - none
---

## Prompt

```text
$ARGUMENTS
```

Project: Todo Full-Stack Web Application (Spec-Driven Development)

Core principles:
- Security-first design (authentication, authorization, user isolation)
- Correctness of business logic and API behavior
- Clear separation of concerns (frontend, backend, database, auth)
- Spec-driven, deterministic implementation
- Scalability and maintainability using modern web standards

Key standards:
- All API behavior must strictly follow the defined REST contract
- Authentication must use Better Auth with JWT-based verification
- Every request must be authorized and scoped to the authenticated user
- Database operations must enforce task ownership at query level
- Frontend must consume APIs only through authenticated requests
- No feature behavior may diverge from the specification

Constraints:
- Technology stack is fixed:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth with JWT
- Stateless authentication using JWT only
- Shared JWT secret via environment variable (BETTER_AUTH_SECRET)
- No cross-user data access under any circumstance
- REST APIs must return proper HTTP status codes
- Persistent storage required (no in-memory data)

Security constraints:
- All endpoints require a valid JWT token
- Requests without a valid token must return 401 Unauthorized
- User identity must be derived from JWT, not client input
- URL user_id must match authenticated user
- Tokens must support expiration
- No sensitive data leakage in errors or logs

Quality standards:
- Clean, readable, and well-structured code
- Explicit request/response validation
- Clear error handling paths
- Modular design across specs
- Environment-based configuration for secrets

Success criteria:
- Users can securely sign up and sign in
- Authenticated users can only see and manage their own tasks
- All CRUD task operations work as specified
- JWT authentication works across frontend and backend
- Database persists data correctly across sessions
- Application behaves correctly under multi-user usage
- All specs are implemented without violating constraints

## Response snapshot

I have successfully updated the project constitution and aligned all related templates with the specified principles for the Todo Full-Stack Web Application. Here's what was accomplished:

1. Created a new constitution file at `.specify/memory/constitution.md` with all the specified principles, constraints, security requirements, and success criteria.

2. Updated the plan template to include:
   - Constitution compliance checks for security, correctness, separation of concerns, etc.
   - Specific technology stack details as mandated by the constitution
   - Proper project structure reflecting the web application architecture

3. Updated the spec template to include:
   - Functional requirements that emphasize authentication, authorization, and data isolation
   - Success criteria aligned with the project's security and functionality goals

4. Updated the tasks template to include:
   - Foundational tasks for authentication framework and database setup
   - Implementation tasks that emphasize security and proper architecture
   - Security hardening tasks in the final phase

5. Updated the ADR template to:
   - Reflect the fixed technology stack constraints
   - Emphasize that deviations from the constitution require special approval

6. Updated the PHR template to:
   - Include compliance checks for security and data isolation
   - Ensure all changes align with the project constitution

7. Created a comprehensive README.md file that:
   - Explains the project constitution and principles
   - Documents the project structure
   - Provides setup instructions aligned with the technology stack

All templates now properly reflect the security-first design, authentication requirements, and technology stack constraints specified in the constitution.

## Outcome

- ✅ Impact: Established project constitution with all required principles and constraints
- 🧪 Tests: No tests required for this configuration task
- 📁 Files: Updated constitution file and all related templates
- 🔁 Next prompts: Ready for feature specification and implementation
- 🧠 Reflection: All templates now align with the project's security and architectural requirements

## Compliance Check

- 🔐 Security: All changes comply with authentication and authorization requirements
- 🛡️ Data Isolation: All changes maintain proper user data separation
- ✅ Constitution: All changes align with project constitution principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A for this configuration task
- Prompt variant (if applicable): Standard constitution setup
- Next experiment (smallest change to try): Begin feature specification using the new templates