'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import SignInForm from '@/src/components/auth/SignInForm';
import { apiClient } from '@/src/app/api/client';
import { User } from '@/src/lib/types';
import { setAuthToken, setUserData } from '@/src/lib/auth';
import { isValidEmail } from '@/src/lib/utils';

const SignInPage: React.FC = () => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSignIn = async (formData: { email: string; password: string }) => {
    // ✅ Client-side validation
    if (!isValidEmail(formData.email)) {
      setError('Please enter a valid email address');
      return;
    }

    if (!formData.password) {
      setError('Password is required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // ✅ API call
      const response = await apiClient.authPost<{
        user: User;
        token: string;
      }>('/auth/signin', {
        email: formData.email,
        password: formData.password,
      });

      if (response.error) {
        setError(response.error);
        return;
      }

      if (response.data) {
        // ✅ Store auth data
        if (typeof window !== 'undefined') {
          setAuthToken(response.data.token);
          setUserData(response.data.user);
        }

        // ✅ IMPORTANT: redirect to dashboard
        router.push('/dashboard');

        // ✅ force rerender so useAuth updates
        router.refresh();
      }
    } catch (err: any) {
      setError(err?.message || 'An error occurred during sign in');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center
      bg-gradient-to-br from-blue-50 to-indigo-100
      dark:from-gray-900 dark:to-gray-950
      py-12 px-4 sm:px-6 lg:px-8
      transition-colors duration-300"
    >
      <SignInForm
        onSignIn={handleSignIn}
        loading={loading}
        error={error}
      />
    </div>
  );
};

export default SignInPage;
