# Todo Full-Stack Web Application

Welcome to the Todo Full-Stack Web Application project. This is a modern multi-user web application built with Next.js, FastAPI, and Neon Serverless PostgreSQL, featuring secure authentication with Better Auth.

## Project Constitution

This project operates under a constitution that defines our core principles and constraints. Please familiarize yourself with these principles:

### Core Principles

1. **Security-First Design**: All system components prioritize security from initial design through implementation. Authentication and authorization mechanisms are implemented at every layer, with user data isolation enforced to prevent cross-user access.

2. **Correctness of Business Logic**: All API behavior strictly follows defined REST contracts. Business logic is validated against specifications before implementation, and every feature behaves as specified with no deviation.

3. **Clear Separation of Concerns**: Frontend, backend, database, and authentication layers remain independent. Each component has well-defined interfaces and responsibilities, with code organization reflecting architectural boundaries.

4. **Spec-Driven Implementation**: All development follows the defined specifications. Implementation is deterministic and follows testable requirements, with features built according to spec without additional functionality.

5. **Scalability and Maintainability**: Code uses modern web standards for long-term maintainability. System architecture supports growth in users and features, with implementation following clean code principles for scalability.

### Technology Stack (Fixed)

- **Frontend**: Next.js 16+ (App Router)
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT

### Security Constraints

- All endpoints require a valid JWT token
- Requests without a valid token return 401 Unauthorized
- User identity is derived from JWT, not client input
- URL user_id must match authenticated user
- Tokens support expiration
- No sensitive data leakage in errors or logs

## Project Structure

```
backend/
├── src/
│   ├── models/          # SQLModel database models
│   ├── services/        # Business logic services
│   ├── api/             # FastAPI endpoints
│   └── auth/            # Better Auth integration
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── app/             # Next.js 16+ App Router pages
│   ├── components/      # React components
│   ├── lib/             # Shared utilities and services
│   └── hooks/           # Custom React hooks
└── tests/
    ├── unit/
    └── integration/

shared/
├── types/               # Shared TypeScript types
└── constants/           # Shared constants and configuration
```

## Getting Started

### Prerequisites

- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- Access to Neon Serverless PostgreSQL database

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo-fullstack-app
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

4. Configure environment variables:
   Create `.env` files in both backend and frontend with the required configuration values, including the JWT secret for Better Auth.

5. Run the applications:
   - Backend: `cd backend && python -m src.main`
   - Frontend: `cd frontend && npm run dev`

## Development Guidelines

- All API behavior must strictly follow the defined REST contract
- Authentication must use Better Auth with JWT-based verification
- Every request must be authorized and scoped to the authenticated user
- Database operations must enforce task ownership at query level
- Frontend must consume APIs only through authenticated requests
- No feature behavior may diverge from the specification

## Contributing

When contributing to this project, please ensure your changes align with the project constitution and follow the established patterns in the codebase. All contributions should include appropriate tests and documentation.

## License

This project is licensed under the MIT License - see the LICENSE file for details.