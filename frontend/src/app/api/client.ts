"use client";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://hiba-05-todoapp-phase-2.hf.space";

// Define types
export interface User {
  id: string;
  email: string;
}

export interface AuthResponse {
  success: boolean;
  user: User;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed';
  user_id?: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed';
  user_id?: string;
}

// Simple API response type
interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export const apiClient = {
  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${API_BASE_URL}${endpoint}`;

      const response = await fetch(url, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
      });

      let data: any = null;
      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        return { error: data?.message || "Request failed" };
      }

      return { data };
    } catch (error) {
      console.error("Fetch failed:", error);
      return {
        error:
          "Backend unreachable. Check backend server, port, and CORS.",
      };
    }
  },

  get<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: "GET" });
  },

  post<T>(endpoint: string, body: any) {
    return this.request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  put<T>(endpoint: string, body: any) {
    return this.request<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
    });
  },

  delete<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: "DELETE" });
  },
};

// Auth API functions
export const authAPI = {
  async signup(email: string, password: string): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/signup', {
      email,
      password
    });

    if (response.error) {
      throw new Error(response.error);
    }

    if (!response.data) {
      throw new Error('No response data received');
    }

    return response.data;
  },

  async signin(email: string, password: string): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/signin', {
      email,
      password
    });

    if (response.error) {
      throw new Error(response.error);
    }

    if (!response.data) {
      throw new Error('No response data received');
    }

    return response.data;
  }
};

// Tasks API functions
export const tasksAPI = {
  async getTasks(): Promise<Task[]> {
    const response = await apiClient.get<Task[]>('/api/v1/tasks/');

    if (response.error) {
      throw new Error(response.error);
    }

    if (!response.data) {
      throw new Error('No response data received');
    }

    return response.data;
  },

  async createTask(task: TaskCreate): Promise<Task> {
    const response = await apiClient.post<Task>('/api/v1/tasks/', task);

    if (response.error) {
      throw new Error(response.error);
    }

    if (!response.data) {
      throw new Error('No response data received');
    }

    return response.data;
  },

  async updateTask(id: string, updates: Partial<Task>): Promise<Task> {
    const response = await apiClient.put<Task>(`/api/v1/tasks/${id}`, updates);

    if (response.error) {
      throw new Error(response.error);
    }

    if (!response.data) {
      throw new Error('No response data received');
    }

    return response.data;
  },

  async deleteTask(id: string): Promise<void> {
    const response = await apiClient.delete(`/api/v1/tasks/${id}`);

    if (response.error) {
      throw new Error(response.error);
    }
  }
};
