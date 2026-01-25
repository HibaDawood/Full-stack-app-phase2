/**
 * Utility functions for handling authentication tokens
 * Note: Current implementation stores user data in localStorage instead of using JWT tokens
 */

// Function to get the current user from localStorage (acts as our "token")
export const getCurrentUser = (): any => {
  if (typeof window !== 'undefined') {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  }
  return null;
};

// Function to store the user data in localStorage
export const storeUser = (user: any): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('user', JSON.stringify(user));
  }
};

// Function to remove the user data from localStorage
export const removeUser = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('user');
  }
};

// Function to check if the current user data is valid
export const isUserValid = (): boolean => {
  const user = getCurrentUser();
  
  // Check if user exists
  if (!user) {
    return false;
  }

  // In the current implementation, we're not using expiring tokens
  // So we just check if the user object has the required properties
  return user.id && user.email;
};

// Main function to get a valid user, essentially checking if the user session is valid
export const getValidUser = (): any | null => {
  const user = getCurrentUser();

  if (!user) {
    return null; // No user available
  }

  // Check if the user data is valid
  if (isUserValid()) {
    // User is still valid
    return user;
  }

  // User data is invalid, remove it
  removeUser();
  return null;
};

// Function to get the auth token (in current implementation, we return the user ID as a form of identification)
export const getValidToken = (): string | null => {
  const user = getValidUser();
  return user ? user.id : null;
};