'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/Card';
import { isValidEmail } from '@/lib/utils';
import { SignInForm as SignInFormType } from '@/lib/types';

interface SignInFormProps {
  onSignIn: (formData: SignInFormType) => void;
  loading?: boolean;
  error?: string | null;
}

const SignInForm: React.FC<SignInFormProps> = ({ onSignIn, loading = false, error = null }) => {
  const [formData, setFormData] = useState<SignInFormType>({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<Partial<SignInFormType>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (errors[name as keyof SignInFormType]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<SignInFormType> = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onSignIn(formData);
    }
  };

  return (
    <div className="w-full max-w-md">
      <Card className="relative overflow-hidden border-0 shadow-xl bg-gradient-to-br from-white to-gray-50 dark:from-gray-900 dark:to-gray-950">
        <div className="absolute inset-0 bg-grid-pattern opacity-[0.03] dark:opacity-[0.05]"></div>
        <CardHeader className="relative z-10 text-center pb-4">
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Welcome Back
          </CardTitle>
          <CardDescription className="text-gray-600 dark:text-gray-400 mt-2">
            Sign in to your account to continue your productivity journey
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="relative z-10 space-y-5 pt-2">
            {error && (
              <div className="p-3.5 bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900/50 text-red-700 dark:text-red-400 rounded-lg text-sm transition-all duration-300">
                {error}
              </div>
            )}

            <div className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="your@email.com"
                  value={formData.email}
                  onChange={handleChange}
                  className={`h-12 rounded-xl border-0 bg-gray-50 dark:bg-gray-800/50 backdrop-blur-sm px-4 py-3 text-base transition-all duration-300 focus:ring-2 focus:ring-blue-500 focus:shadow-lg ${errors.email ? 'focus:ring-red-500' : ''}`}
                />
                {errors.email && <p className="text-red-500 text-xs mt-1.5 ml-0.5">{errors.email}</p>}
              </div>

              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                  className={`h-12 rounded-xl border-0 bg-gray-50 dark:bg-gray-800/50 backdrop-blur-sm px-4 py-3 text-base transition-all duration-300 focus:ring-2 focus:ring-blue-500 focus:shadow-lg ${errors.password ? 'focus:ring-red-500' : ''}`}
                />
                {errors.password && <p className="text-red-500 text-xs mt-1.5 ml-0.5">{errors.password}</p>}
              </div>
            </div>
          </CardContent>
          <CardFooter className="relative z-10 flex flex-col gap-4 pt-2">
            <Button
              type="submit"
              className="w-full h-12 rounded-xl text-base font-semibold transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg hover:shadow-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              disabled={loading}
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Signing In...
                </span>
              ) : 'Sign In'}
            </Button>
            <p className="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
              Don't have an account?{' '}
              <a href="/auth/signup" className="text-blue-600 dark:text-blue-400 font-medium hover:underline transition-all duration-200">
                Sign up
              </a>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
};

export default SignInForm;