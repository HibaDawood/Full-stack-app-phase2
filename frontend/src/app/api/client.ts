"use client";

import { handleUnauthorizedAccess, handleForbiddenAccess } from '@/src/lib/auth';
import { getValidToken } from '@/src/lib/tokenUtils';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000" || "https://hiba-05-todo-app-phase2.hf.space/";
const API_V1_BASE_URL = `${API_BASE_URL}/api/v1`;

// Define the shape of our API response
interface ApiResponse<T> {
  data?: T;
  error?: string;
}

// Generic API client with JWT token handling
export const apiClient = {
  // Generic request function that handles JWT tokens
  async request<T>(
    endpoint: string,
    options: RequestInit = {},
    useV1Base: boolean = true // Whether to use the /api/v1 base URL or the root base URL
  ): Promise<ApiResponse<T>> {
    try {
      // Get a valid JWT token (this will refresh if needed)
      const token = await getValidToken();

      // Set up default headers
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",  // Helps identify client requests
        "X-Client-Type": "web",               // Identifies the client type
        ...(options.headers as Record<string, string> || {}),
      };

      // Add authorization header if token exists
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }

      // Determine the base URL based on the endpoint type
      const baseURL = useV1Base ? API_V1_BASE_URL : API_BASE_URL;
      const url = `${baseURL}${endpoint}`;

      console.log(`Making request to: ${url}`); // Debug logging
      console.log(`Headers:`, headers); // Debug logging
      console.log(`Token:`, token ? 'Present' : 'Missing'); // Debug logging

      // Make the request
      const response = await fetch(url, {
        ...options,
        headers,
      });

      console.log(`Response status: ${response.status}`); // Debug logging

      // Handle 401 Unauthorized responses
      if (response.status === 401) {
        console.error("Unauthorized access - token may be invalid or expired");
        handleUnauthorizedAccess();
        return { error: "Unauthorized: Please log in again" };
      }

      // Handle 403 Forbidden responses
      if (response.status === 403) {
        console.error("Forbidden access - you don't have permission for this resource");
        handleForbiddenAccess();
        return { error: "Forbidden: You don't have permission for this resource" };
      }

      // Try to parse the response as JSON
      let data;
      try {
        data = await response.json();
        console.log(`Response data:`, data); // Debug logging
      } catch (e) {
        // If response is not JSON, return status message
        console.warn(`Response not JSON:`, response.statusText); // Debug logging
        data = { message: response.statusText };
      }

      // Return appropriate response based on success/failure
      if (!response.ok) {
        return { error: data.message || "An error occurred" };
      }

      return { data };
    } catch (error: any) {
      console.error("API request failed:", error);
      console.error("Error details:", {
        message: error.message,
        stack: error.stack,
        name: error.name
      });

      // Check if it's a network error
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return { error: "Network error: Unable to connect to the server. Please check if the backend is running." };
      }

      return { error: error.message || "Network error" };
    }
  },

  // Auth request function for endpoints that don't use /api/v1 prefix
  async authRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, options, false); // Don't use V1 base for auth endpoints
  },

  // V1 request function for endpoints that use /api/v1 prefix
  async v1Request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, options, true); // Use V1 base for API v1 endpoints
  },

  // GET request helper for API v1 endpoints
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.v1Request<T>(endpoint, { method: "GET" });
  },

  // POST request helper for API v1 endpoints
  async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.v1Request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  // PUT request helper for API v1 endpoints
  async put<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.v1Request<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
    });
  },

  // DELETE request helper for API v1 endpoints
  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.v1Request<T>(endpoint, { method: "DELETE" });
  },

  // Auth-specific helpers
  async authPost<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.authRequest<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },
};