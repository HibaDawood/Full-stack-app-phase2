

import { User } from './types';

// Utility function to get the user data
export const getUserData = () => {
  if (typeof window !== 'undefined') {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  }
  return null;
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

// Utility function to clear all authentication data
export const clearAuthData = (): void => {
  removeUserData();
};

// Utility function to handle unauthorized access attempts
export const handleUnauthorizedAccess = (): void => {
  if (typeof window !== 'undefined') {
    // Clear authentication data
    localStorage.removeItem('user');

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

    // Optionally redirect to tasks or home page
    window.location.href = '/tasks';
  }
};