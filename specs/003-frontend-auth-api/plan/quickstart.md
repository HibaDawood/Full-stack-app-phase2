# Quickstart Guide: Frontend UI & Auth Integration

**Feature**: Frontend UI & Auth Integration
**Created**: 2026-01-08
**Status**: Draft

## Prerequisites

Before getting started, ensure you have the following installed:

- Node.js 18 or higher
- npm, yarn, and/or pnpm package manager
- Git
- Access to the backend API
- BETTER_AUTH_SECRET environment variable

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies
Using npm:
```bash
npm install
```

Or using yarn:
```bash
yarn install
```

Or using pnpm:
```bash
pnpm install
```

### 3. Environment Configuration
Copy the example environment file and configure your settings:
```bash
cp .env.example .env.local
```

Edit the `.env.local` file with your specific configurations:
```bash
# Backend API configuration
NEXT_PUBLIC_API_BASE_URL=.http://0.0.0.0:8000/

# Better Auth configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://0.0.0.0:8000/
B
# Other configurations
NEXT_PUBLIC_APP_NAME="Todo App"
```

### 4. Run the Application
Start the development server:
```bash
# Using npm
npm run dev

# Using yarn
yarn dev

# Using pnpm
pnpm dev
```

The application will be available at `http://localhost:3000`.

## API Usage

Once the server is running, you can access the application at `http://localhost:3000`.

### Authentication Flow
1. Navigate to `/signup` to create a new account
2. Use your credentials to sign in at `/signin`
3. After successful authentication, you'll be redirected to the dashboard
4. Your JWT token will be automatically included in all authenticated API requests

### Task Management
1. On the dashboard, you can view all your tasks
2. Use the "Create Task" button to add new tasks
3. Click on a task to edit its details or mark it as complete
4. Use the delete button to remove tasks

## Running Tests

### Unit Tests
```bash
# Run all unit tests
npm run test

# Run with coverage
npm run test -- --coverage
```

### Component Tests
```bash
# Run component tests
npm run test:components

# Run with watch mode
npm run test:components -- --watch
```

### E2E Tests
```bash
# Run end-to-end tests
npm run test:e2e
```

## Development Workflow

### Code Structure
The frontend follows this structure:
```
frontend/
├── app/
│   ├── layout.tsx              # Root layout with navbar
│   ├── page.tsx                # Landing page
│   ├── globals.css             # Global styles
│   ├── providers.tsx           # Context providers
│   ├── api/
│   │   └── client.ts           # API client with JWT handling
│   ├── auth/
│   │   ├── layout.tsx          # Auth layout
│   │   ├── signin/
│   │   │   └── page.tsx        # Signin page
│   │   ├── signup/
│   │   │   └── page.tsx        # Signup page
│   │   └── signout/
│   │       └── page.tsx        # Signout page
│   ├── dashboard/
│   │   ├── layout.tsx          # Dashboard layout
│   │   └── page.tsx            # Dashboard page
│   ├── tasks/
│   │   ├── layout.tsx          # Tasks layout
│   │   └── page.tsx            # Tasks page
│   └── middleware.ts           # Authentication middleware
├── components/
│   ├── ui/                     # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── ...
│   ├── auth/                   # Authentication components
│   │   ├── SignInForm.tsx
│   │   ├── SignUpForm.tsx
│   │   └── ...
│   ├── tasks/                  # Task management components
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskModal.tsx
│   │   └── ...
│   └── layout/                 # Layout components
│       ├── Navbar.tsx
│       └── ...
├── lib/
│   ├── auth.ts                 # Authentication utilities
│   ├── types.ts                # Type definitions
│   └── utils.ts                # Utility functions
├── hooks/
│   ├── useAuth.ts              # Authentication hook
│   └── useTasks.ts             # Tasks management hook
├── public/
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

### Adding New Components
1. Create the component in the appropriate directory under `components/`
2. Export the component from its file
3. Import and use the component in your pages or other components
4. Write tests for the new component
5. Update documentation if needed

### Adding New API Endpoints
1. Add the endpoint to the API client in `app/api/client.ts`
2. Create appropriate TypeScript types for request/response
3. Handle the endpoint in your components or hooks
4. Write tests for the new API integration

## Troubleshooting

### Common Issues

#### Authentication Issues
- Verify that the `BETTER_AUTH_SECRET` matches between frontend and backend
- Check that JWT tokens are properly stored and sent with requests
- Ensure the authentication middleware is properly configured

#### API Communication Issues
- Verify that the `NEXT_PUBLIC_API_BASE_URL` is correctly set
- Check that the backend server is running and accessible
- Confirm that JWT tokens are properly attached to authenticated requests

#### Responsive Design Issues
- Test the application on different screen sizes
- Verify that Tailwind CSS classes are properly applied
- Check that mobile-first approach is followed consistently

## Deployment

### Environment Variables for Production
```
NEXT_PUBLIC_API_BASE_URL=https:/api.yourdomain.com
NEXT_PUBLIC_BETTER_AUTH_URL=https:/auth.yourdomain.com
BETTER_AUTH_SECRET=production_jwt_secret
NEXT_PUBLIC_APP_NAME="Production Todo App"
```

### Build and Run
```bash
# Build the application
npm run build

# Run the production server
npm start
```

### Docker Deployment (Optional)
If Docker support is added:
```bash
# Build the image
docker build -t todo-frontend .

# Run the container
docker run -d -p 3000:3000 --env-file .env todo-frontend
```