'use client';

import React, { useState } from 'react';
import SignUpForm from '@/src/components/auth/SignUpForm';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/src/app/api/client';
import { User } from '@/src/lib/types';
import { setAuthToken, setUserData } from '@/src/lib/auth';
import { isValidEmail, isValidPassword } from '@/src/lib/utils';

const SignUpPage: React.FC = () => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSignUp = async (formData: { email: string; password: string; confirmPassword: string }) => {
    // Perform client-side validation
    if (!isValidEmail(formData.email)) {
      setError('Please enter a valid email address');
      return;
    }

    if (!isValidPassword(formData.password)) {
      setError('Password must be at least 8 characters long');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Call the API to register the user
      const response = await apiClient.authPost<{ user: User; token: string }>('/auth/signup', {
        email: formData.email,
        password: formData.password,
      });

      if (response.error) {
        setError(response.error);
        setLoading(false);
        return;
      }

      if (response.data) {
        // Store the token and user data in localStorage
        if (typeof window !== 'undefined') {
          setAuthToken(response.data.token);
          setUserData(response.data.user);
        }

        // Redirect to the dashboard
        router.push('/dashboard');
        router.refresh(); // Refresh to update the UI based on auth state
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred during registration');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-950 py-12 px-4 sm:px-6 lg:px-8 transition-colors duration-300">
      <SignUpForm onSignUp={handleSignUp} loading={loading} error={error} />
    </div>
  );
};

export default SignUpPage;