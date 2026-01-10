

import { User } from './types';

// Utility function to get the user data
export const getUserData = () => {
  if (typeof window !== 'undefined') {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  }
  return null;
};

// Utility function to set the auth token
export const setAuthToken = (token: string | null): void => {
  if (typeof window !== 'undefined') {
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }
};

// Utility function to get the auth token
export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
};

// Utility function to remove the auth token
export const removeAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
    delete (window as any).apiClient.defaults.headers.common['Authorization'];
  }
};

// Utility function to set the user data
export const setUserData = (user: User): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('user', JSON.stringify(user));
  }
};

// Utility function to remove the user data
export const removeUserData = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('user');
  }
};

// Utility function to check if user is authenticated


// Utility function to clear all authentication data
export const clearAuthData = (): void => {

  removeUserData();
  removeAuthToken();
};

// Utility function to validate JWT token (basic validation)
export const isTokenValid = (token: string | null): boolean => {
  if (!token) return false;

  try {
    // Split the token to get the payload
    const parts = token.split('.');
    if (parts.length !== 3) return false;

    // Decode the payload (second part)
    const payload = JSON.parse(atob(parts[1]));

    // Check if token is expired
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp > currentTime;
  } catch (error) {
    console.error('Error validating token:', error);
    return false;
  }
};

// Utility function to get token expiration time
export const getTokenExpirationTime = (token: string | null): number | null => {
  if (!token) return null;

  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    const payload = JSON.parse(atob(parts[1]));
    return payload.exp;
  } catch (error) {
    console.error('Error getting token expiration:', error);
    return null;
  }
};

// Utility function to handle unauthorized access attempts
export const handleUnauthorizedAccess = (): void => {
  if (typeof window !== 'undefined') {
    // Clear authentication data
    clearAuthData();

    // Show user-friendly error message
    alert('Your session has expired or you are not authorized to access this resource. Please sign in again.');

    // Redirect to sign-in page
    window.location.href = '/auth/signin';
  }
};

// Utility function to handle forbidden access attempts
export const handleForbiddenAccess = (): void => {
  if (typeof window !== 'undefined') {
    // Show user-friendly error message
    alert('You do not have permission to access this resource.');

    // Optionally redirect to dashboard or home page
    window.location.href = '/dashboard';
  }
};