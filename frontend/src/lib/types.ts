// User entity type definition
export interface User {
  id: string; // UUID format
  email: string;
  created_at: string; // ISO date format
  updated_at: string; // ISO date format
}

// Task entity type definition
export interface Task {
  id: string; // UUID format
  title: string; // Required, max length 255
  description?: string; // Optional
  status: 'pending' | 'in-progress' | 'completed'; // Allowed values
  user_id: string; // UUID format, reference to user
  created_at: string; // ISO date format
  updated_at: string; // ISO date format
}

// API Response Models
export interface AuthResponse {
  user: User;
  token: string; // JWT token
  expires_at: string; // ISO date format
}

export interface TaskListResponse {
  tasks: Task[];
}

export interface TaskResponse {
  task: Task;
}

// Form Models
export interface SignUpForm {
  email: string; // Required, valid email format
  password: string; // Required, min length 8
  confirmPassword: string; // Required, must match password
}

export interface SignInForm {
  email: string; // Required, valid email format
  password: string; // Required
}

export interface TaskForm {
  title: string; // Required, max length 255
  description?: string; // Optional
  status?: 'pending' | 'in-progress' | 'completed'; // Optional, default "pending"
}

// Frontend State Models
export interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

export interface TaskState {
  tasks: Task[];
  selectedTask: Task | null;
  isLoading: boolean;
  error: string | null;
  isCreating: boolean;
  isUpdating: boolean;
  isDeleting: boolean;
}

// API Client Response
export interface ApiResponse<T> {
  data?: T;
  error?: string;
}