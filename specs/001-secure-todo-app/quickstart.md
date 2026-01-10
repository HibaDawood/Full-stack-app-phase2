# Quickstart Guide: Secure Todo Full-Stack Web Application

## Overview
This guide provides step-by-step instructions to set up, configure, and run the secure todo application locally.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- Access to Neon Serverless PostgreSQL database
- Git for version control

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-fullstack-app
```

### 2. Set Up Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Frontend
```bash
cd ../frontend
npm install
```

### 4. Configure Environment Variables

#### Backend Configuration
Create a `.env` file in the `backend` directory:
```env
DATABASE_URL=postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
BETTER_AUTH_URL=http://localhost:3000
```

#### Frontend Configuration
Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 5. Initialize Database
```bash
cd backend
python -m src.db.init  # This will create tables based on SQLModel definitions
```

### 6. Run the Applications

#### Backend (in one terminal):
```bash
cd backend
python -m src.main
```
The backend will start on `http://localhost:8000`.

#### Frontend (in another terminal):
```bash
cd frontend
npm run dev
```
The frontend will start on `http://localhost:3000`.

## Verification Steps

### 1. Test Authentication Flow
1. Navigate to `http://localhost:3000/signup`
2. Register a new account
3. Verify you're redirected to the dashboard
4. Check that a JWT token is stored in browser's localStorage/sessionStorage

### 2. Test Task Operations
1. Log in to the application
2. Create a new task
3. Verify the task appears in your list
4. Update the task
5. Mark the task as complete
6. Delete the task

### 3. Test Security Isolation
1. Register two different user accounts
2. Have each user create tasks
3. Verify that User A cannot see User B's tasks and vice versa

### 4. Test API Endpoints
Using a tool like curl or Postman:
```bash
# Test protected endpoint without token (should return 401)
curl -X GET http://localhost:8000/api/tasks

# Test protected endpoint with valid token (should return tasks)
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify your Neon Serverless PostgreSQL connection string is correct
- Ensure your database allows connections from your IP address
- Check that SSL mode is properly configured

#### Authentication Problems
- Confirm that `BETTER_AUTH_SECRET` is identical in both frontend and backend
- Verify that JWT tokens are being properly attached to API requests
- Check that the Better Auth configuration matches between frontend and backend

#### CORS Issues
- Ensure your frontend URL is properly configured in the backend CORS settings
- Check that API requests are being made to the correct endpoints

## Next Steps
1. Explore the API documentation at `http://localhost:8000/docs`
2. Review the data models in `specs/001-secure-todo-app/data-model.md`
3. Examine the API contracts in `specs/001-secure-todo-app/contracts/api-contracts.md`
4. Run the test suite to verify all functionality