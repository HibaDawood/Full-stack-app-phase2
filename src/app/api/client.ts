
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

console.log('API_BASE_URL:', API_BASE_URL); 

export interface UserCredentials {
  email: string;
  password: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: string;  // Changed from completed to status
  user_id?: number;
}

export interface SignUpResponse {
  token: string;
  user: {
    id: string;
    email: string;
  };
}

export interface SignInResponse {
  token: string;
  user: {
    id: string;
    email: string;
  };
}

export interface TaskCreateData {
  title: string;
  description?: string;
  user_id?: number;
}

// Generic request function with better error handling
async function request<T>(endpoint: string, options?: RequestInit, token?: string): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  console.log(`Making request to: ${url}`); // Debug log
  console.log('Request options:', options); // Debug log

  try {
    const headers: any = {
      "Content-Type": "application/json",
      ...options?.headers,
    };

    // Add authorization header if token is provided
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    console.log(`Response status: ${response.status}`); // Debug log

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Request failed with status ${response.status}:`, errorText); // Debug log
      throw new Error(`HTTP error! Status: ${response.status}. Details: ${errorText}`);
    }

    const data = await response.json();
    console.log('Response data:', data); // Debug log
    return data;
  } catch (error) {
    console.error('Network error:', error); // Debug log
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Failed to connect to the backend server. Please ensure the backend is running on ' + API_BASE_URL);
    }
    throw error;
  }
}

// Auth API functions
export const authAPI = {
  async signUp(credentials: UserCredentials): Promise<SignUpResponse> {
    return request('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });
  },

  async signIn(credentials: UserCredentials): Promise<SignInResponse> {
    return request('/auth/signin', {
      method: 'POST',
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });
  },
};

// Tasks API functions
export const tasksAPI = {
  async createTask(taskData: TaskCreateData, token?: string): Promise<Task> {
    return request('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    }, token);
  },

  async getTasks(userId?: number, token?: string): Promise<Task[]> {
    let endpoint = '/api/v1/tasks';
    if (userId) {
      endpoint += `?user_id=${userId}`;
    }
    return request(endpoint, undefined, token);
  },

  async updateTask(id: number, taskData: Partial<Task>, token?: string): Promise<Task> {
    return request(`/api/v1/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    }, token);
  },

  async deleteTask(id: number, token?: string): Promise<void> {
    await request(`/api/v1/tasks/${id}`, {
      method: 'DELETE',
    }, token);
  },
};