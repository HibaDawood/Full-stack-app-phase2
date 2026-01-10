'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/src/components/ui/Button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/src/components/ui/Card';
import { Input } from '@/src/components/ui/Input';
import { apiClient } from '@/src/app/api/client';
import { User } from '@/src/lib/types';
import { isValidEmail, isValidPassword } from '@/src/lib/utils';
import { useAuth } from '@/src/hooks/useAuth';
import { useTasks } from '@/src/hooks/useTasks';
import TaskList from '@/src/components/tasks/TaskList';
import TaskModal from '@/src/components/tasks/TaskModal';

const HomePage: React.FC = () => {
  const router = useRouter();
  const { user, isLoading, signIn, signUp, signOut } = useAuth();
  const { tasks, loading, error, createTask, updateTask, deleteTask, toggleTaskCompletion } = useTasks();
  const [isSignUpMode, setIsSignUpMode] = useState(false);
  const [authForm, setAuthForm] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [authError, setAuthError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState<any>(null);

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError(null);

    // Perform client-side validation
    if (!isValidEmail(authForm.email)) {
      setAuthError('Please enter a valid email address');
      return;
    }

    if (!isValidPassword(authForm.password)) {
      setAuthError('Password must be at least 8 characters long');
      return;
    }

    if (isSignUpMode && authForm.password !== authForm.confirmPassword) {
      setAuthError('Passwords do not match');
      return;
    }

    try {
      if (isSignUpMode) {
        await signUp({
          email: authForm.email,
          password: authForm.password,
          confirmPassword: authForm.confirmPassword
        });
      } else {
        await signIn({
          email: authForm.email,
          password: authForm.password
        });
      }
    } catch (err: any) {
      setAuthError(err.message || 'An error occurred during authentication');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setAuthForm(prev => ({ ...prev, [name]: value }));
  };

  const handleCreateTask = () => {
    setEditingTask(null);
    setShowModal(true);
  };

  const handleEditTask = (task: any) => {
    setEditingTask(task);
    setShowModal(true);
  };

  const handleSaveTask = async (taskData: { title: string; description?: string; status?: string }) => {
    const validStatus = (taskData.status as 'pending' | 'in-progress' | 'completed') || 'pending';

    if (editingTask) {
      // Update existing task
      await updateTask(editingTask.id, {
        ...taskData,
        status: validStatus
      });
    } else {
      // Create new task
      await createTask({
        ...taskData,
        status: validStatus
      });
    }

    setShowModal(false);
    setEditingTask(null);
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    await deleteTask(taskId);
  };

  const handleCompleteTask = async (taskId: string) => {
    await toggleTaskCompletion(taskId);
  };

  // If still loading auth state, show loading indicator
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // If user is not authenticated, show auth forms
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <Card className="w-full max-w-md mx-auto">
          <CardHeader>
            <CardTitle>{isSignUpMode ? 'Sign Up' : 'Sign In'}</CardTitle>
            <CardDescription>
              {isSignUpMode
                ? 'Create an account to get started'
                : 'Welcome back! Please sign in to your account'}
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleAuthSubmit}>
            <CardContent className="space-y-4">
              {authError && (
                <div className="p-3 bg-red-100 text-red-700 rounded-md text-sm">
                  {authError}
                </div>
              )}

              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium">Email</label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="your@email.com"
                  value={authForm.email}
                  onChange={handleInputChange}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium">Password</label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  placeholder="••••••••"
                  value={authForm.password}
                  onChange={handleInputChange}
                />
              </div>

              {isSignUpMode && (
                <div className="space-y-2">
                  <label htmlFor="confirmPassword" className="text-sm font-medium">Confirm Password</label>
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    placeholder="••••••••"
                    value={authForm.confirmPassword}
                    onChange={handleInputChange}
                  />
                </div>
              )}
            </CardContent>
            <CardFooter className="flex flex-col">
              <Button
                type="submit"
                className="w-full"
              >
                {isSignUpMode ? 'Sign Up' : 'Sign In'}
              </Button>
              <p className="mt-4 text-center text-sm text-gray-600">
                {isSignUpMode ? (
                  <>
                    Already have an account?{' '}
                    <button
                      type="button"
                      className="text-blue-600 hover:underline"
                      onClick={() => setIsSignUpMode(false)}
                    >
                      Sign in
                    </button>
                  </>
                ) : (
                  <>
                    Don't have an account?{' '}
                    <button
                      type="button"
                      className="text-blue-600 hover:underline"
                      onClick={() => setIsSignUpMode(true)}
                    >
                      Sign up
                    </button>
                  </>
                )}
              </p>
            </CardFooter>
          </form>
        </Card>
      </div>
    );
  }

  // If user is authenticated, show tasks UI
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Your Tasks</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">
              Welcome, {user?.email}
            </span>
            <Button
              variant="outline"
              onClick={signOut}
            >
              Sign Out
            </Button>
          </div>
        </div>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Your Tasks</CardTitle>
            <Button onClick={handleCreateTask}>Create Task</Button>
          </CardHeader>
          <CardContent>
            <TaskList
              tasks={tasks}
              onEdit={handleEditTask}
              onDelete={handleDeleteTask}
              onComplete={handleCompleteTask}
              loading={loading}
            />
          </CardContent>
        </Card>

        <TaskModal
          isOpen={showModal}
          onClose={() => {
            setShowModal(false);
            setEditingTask(null);
          }}
          task={editingTask}
          onSave={handleSaveTask}
        />
      </div>
    </div>
  );
};

export default HomePage;