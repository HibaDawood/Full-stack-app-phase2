# Quickstart Guide: Backend API & Database Layer

**Feature**: Backend API & Database Layer
**Created**: 2026-01-08
**Status**: Draft

## Prerequisites

Before getting started, ensure you have the following installed:

- Python 3.9 or higher
- Poetry (recommended) or pip for dependency management
- Git
- Access to Neon Serverless PostgreSQL database
- BETTER_AUTH_SECRET environment variable

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Using Poetry (recommended):
```bash
poetry install
poetry shell
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the example environment file and configure your settings:
```bash
cp .env.example .env
```

Edit the `.env` file with your specific configurations:
```bash
# Database configuration
DATABASE_URL=postgresql://username:password@ep-xxxx.us-east-1.aws.neon.tech/dbname?sslmode=require

# Authentication configuration
BETTER_AUTH_SECRET=your_jwt_secret_key_here

# Other configurations
DEBUG=true
LOG_LEVEL=INFO
```

### 5. Database Setup
Initialize the database and run migrations:
```bash
# Using poetry
poetry run python -m app.database.init

# Or using python directly
python -m app.database.init
```

### 6. Run the Application
Start the development server:
```bash
# Using Uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Using Poetry
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Using the provided script (if available)
poetry run dev
```

## API Usage

Once the server is running, you can access the API at `http://localhost:8000`.

### Authentication
All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Example API Calls

#### Get all tasks for authenticated user
```bash
curl -X GET \
  http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>"
```

#### Create a new task
```bash
curl -X POST \
  http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task description", "status": "pending"}'
```

## Running Tests

### Unit Tests
```bash
# Run all unit tests
poetry run pytest tests/unit/

# Run specific test file
poetry run pytest tests/unit/test_models.py

# Run with coverage
poetry run pytest --cov=app tests/unit/
```

### Integration Tests
```bash
# Run all integration tests
poetry run pytest tests/integration/

# Run with verbose output
poetry run pytest -v tests/integration/
```

### Security Tests
```bash
# Run security-focused tests
poetry run pytest tests/security/
```

## Development Workflow

### Code Structure
The backend follows this structure:
```
app/
├── __init__.py
├── main.py              # FastAPI app instance
├── config.py            # Configuration and settings
├── database.py          # Database engine and session
├── models/              # SQLModel definitions
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── schemas/             # Pydantic models
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── api/                 # API routes
│   ├── __init__.py
│   ├── deps.py          # Dependency injection
│   └── v1/              # API version 1
│       ├── __init__.py
│       └── tasks.py
└── utils/               # Utility functions
    ├── __init__.py
    ├── auth.py          # JWT utilities
    └── exceptions.py    # Custom exceptions
```

### Adding New Endpoints
1. Create the corresponding Pydantic schema in `schemas/`
2. Add the endpoint function in the appropriate file in `api/v1/`
3. Import and include the router in `api/__init__.py`
4. Write tests for the new functionality
5. Update the OpenAPI specification if needed

### Database Migrations
When you modify the models:
1. Install Alembic if not already installed: `poetry add alembic`
2. Initialize Alembic (first time only): `alembic init alembic`
3. Generate a migration: `alembic revision --autogenerate -m "Description of changes"`
4. Apply the migration: `alembic upgrade head`

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify your Neon PostgreSQL connection string is correct
- Ensure your Neon database is active (serverless databases may pause after inactivity)
- Check that your IP is whitelisted if using IP-based access controls

#### JWT Authentication Issues
- Verify that the `BETTER_AUTH_SECRET` matches the one used by Better Auth
- Ensure JWT tokens are properly formatted with "Bearer " prefix
- Check that tokens haven't expired

#### Dependency Issues
- Try clearing the Poetry cache: `poetry cache clear pypi --all`
- Regenerate lock file: `poetry lock --no-update`
- Install dependencies from scratch: `poetry install --no-cache`

## Deployment

### Environment Variables for Production
```
DATABASE_URL=postgresql://username:password@production-neon-db-url
BETTER_AUTH_SECRET=production_jwt_secret
DEBUG=false
LOG_LEVEL=WARNING
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Docker Deployment (Optional)
If Docker support is added:
```bash
# Build the image
docker build -t todo-backend .

# Run the container
docker run -d -p 8000:8000 --env-file .env todo-backend
```