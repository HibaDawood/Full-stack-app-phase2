import { useState, useEffect } from 'react';
import { apiClient } from '@/src/app/api/client';
import { User, AuthState } from '@/src/lib/types';
import { setUserData, removeUserData } from '@/src/lib/auth';

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isLoading: true,
    error: null,
  });

  // Check for existing auth state on initial load
  useEffect(() => {
    const userData = localStorage.getItem('user');

    if (userData) {
      try {
        let user = JSON.parse(userData);

        // Ensure the user object has all required fields
        if (user && typeof user === 'object') {
          user = {
            id: user.id || '',
            email: user.email || '',
            created_at: user.created_at || new Date().toISOString(),
            updated_at: user.updated_at || new Date().toISOString()
          };
        }

        setAuthState({
          user,
          isLoading: false,
          error: null,
        });
      } catch (error) {
        console.error('Failed to parse user data from localStorage:', error);
        // Clear invalid data
        localStorage.removeItem('user');
        setAuthState({
          user: null,
          isLoading: false,
          error: null,
        });
      }
    } else {
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
      }));
    }
  }, []);

  const signUp = async (formData: { email: string; password: string; confirmPassword: string }) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await apiClient.post<{
        success: boolean;
        user: { id: string; email: string };
      }>('/auth/signup', {
        email: formData.email,
        password: formData.password,
      });

      if (response.error) {
        throw new Error(response.error);
      }

      if (response.data) {
        // Create a complete user object that matches the User interface
        const completeUser: User = {
          id: response.data.user.id,
          email: response.data.user.email,
          created_at: new Date().toISOString(), // Use current time as a fallback
          updated_at: new Date().toISOString()  // Use current time as a fallback
        };

        // Store the user data in localStorage
        if (typeof window !== 'undefined') {
          setUserData(completeUser);
        }

        setAuthState({
          user: completeUser,
          isLoading: false,
          error: null,
        });

        return { success: true };
      } else {
        throw new Error('Registration failed');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Registration failed';
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      return { success: false, error: errorMessage };
    }
  };

  const signIn = async (formData: { email: string; password: string }) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await apiClient.post<{
        success: boolean;
        user: { id: string; email: string };
      }>('/auth/signin', {
        email: formData.email,
        password: formData.password,
      });

      if (response.error) {
        throw new Error(response.error);
      }

      if (response.data) {
        // Create a complete user object that matches the User interface
        const completeUser: User = {
          id: response.data.user.id,
          email: response.data.user.email,
          created_at: new Date().toISOString(), // Use current time as a fallback
          updated_at: new Date().toISOString()  // Use current time as a fallback
        };

        // Store the user data in localStorage
        if (typeof window !== 'undefined') {
          setUserData(completeUser);
        }

        setAuthState({
          user: completeUser,
          isLoading: false,
          error: null,
        });

        return { success: true };
      } else {
        throw new Error('Sign in failed');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Sign in failed';
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      return { success: false, error: errorMessage };
    }
  };

  const signOut = async () => {
    try {
      // Call the backend signout endpoint
      await apiClient.post('localhost:3000', {});
    } catch (error) {
      console.error('Signout error:', error);
      // Even if the backend call fails, we should still clear local data
    } finally {
      // Clear the user data from localStorage
      if (typeof window !== 'undefined') {
        removeUserData();
      }

      setAuthState({
        user: null,
        isLoading: false,
        error: null,
      });

      // Redirect to homepage after signout
      window.location.href = '/';
    }
  };

  const updateUser = (userData: Partial<User>) => {
    if (authState.user) {
      const updatedUser = { ...authState.user, ...userData };
      setAuthState(prev => ({
        ...prev,
        user: updatedUser,
      }));

      // Update the user data in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }
    }
  };

  return {
    ...authState,
    signUp,
    signIn,
    signOut,
    updateUser,
  };
};