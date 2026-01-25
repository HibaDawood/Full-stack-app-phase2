'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthState } from '@/src/lib/types';
import { LanguageProvider } from '@/src/contexts/LanguageContext';

// Create contexts for different parts of the state
const AuthContext = createContext<{
  authState: AuthState;
  setAuthState: React.Dispatch<React.SetStateAction<AuthState>>;
}>({
  authState: {
    user: null,
    isLoading: true,
    error: null,
  },
  setAuthState: () => {},
});

// Provider component that wraps the app
export function Providers({ children }: { children: React.ReactNode }) {
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
        const user = JSON.parse(userData);
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

  return (
    <LanguageProvider>
      <AuthContext.Provider value={{ authState, setAuthState }}>
        {children}
      </AuthContext.Provider>
    </LanguageProvider>
  );
}

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};