'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

const SignOutPage: React.FC = () => {
  const router = useRouter();

  useEffect(() => {
    // Clear the authentication token and user data from localStorage
    if (typeof window !== 'undefined') {
      localStorage.removeItem('user');
    }

    // Redirect to the home page or sign in page
    router.push('/');
    router.refresh(); // Refresh to update the UI based on auth state
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Signing Out
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            You are being signed out of your account...
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignOutPage;