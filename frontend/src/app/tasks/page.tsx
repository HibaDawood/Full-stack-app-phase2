'use client';

import React, { useState } from 'react';
import { useAuth } from '@/src/hooks/useAuth';
import { useTasks } from '@/src/hooks/useTasks';
import { Task } from '@/src/lib/types';
import TaskList from '@/src/components/tasks/TaskList';
import TaskModal from '@/src/components/tasks/TaskModal';
import { Button } from '@/src/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/src/components/ui/Card';

const TasksPage: React.FC = () => {
  const { user, signOut } = useAuth();
  const { tasks, loading, error, createTask, updateTask, deleteTask, toggleTaskCompletion } = useTasks();
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const handleCreateTask = () => {
    setEditingTask(null);
    setShowModal(true);
  };

  const handleEditTask = (task: Task) => {
    // Ensure the user can only edit their own tasks
    if (task.user_id !== user?.id) {
      alert('You can only edit your own tasks.');
      return;
    }
    setEditingTask(task);
    setShowModal(true);
  };

  const handleSaveTask = async (taskData: { title: string; description?: string; status?: string }) => {
    const validStatuses = ['pending', 'in-progress', 'completed'] as const;
    const status = (taskData.status && validStatuses.includes(taskData.status as any)) ? (taskData.status as 'pending' | 'in-progress' | 'completed') : 'pending';

    if (editingTask) {
      // Ensure the user can only update their own tasks
      if (editingTask.user_id !== user?.id) {
        alert('You can only update your own tasks.');
        return;
      }
      // Update existing task
      await updateTask(editingTask.id, {
        ...taskData,
        status
      });
    } else {
      // Create new task
      await createTask({
        ...taskData,
        status
      });
    }

    setShowModal(false);
    setEditingTask(null);
  };

  const handleDeleteTask = async (taskId: string) => {
    // Find the task to check ownership, ensuring task is not null/undefined
    const taskToDelete = tasks.find(task => task && task.id === taskId);

    if (!taskToDelete) {
      alert('Task not found.');
      return;
    }

    // Ensure the user can only delete their own tasks
    if (taskToDelete.user_id !== user?.id) {
      alert('You can only delete your own tasks.');
      return;
    }

    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    await deleteTask(taskId);
  };

  const handleCompleteTask = async (taskId: string, completed: boolean) => {
    // Find the task to check ownership, ensuring task is not null/undefined
    const taskToComplete = tasks.find(task => task && task.id === taskId);

    if (!taskToComplete) {
      alert('Task not found.');
      return;
    }

    // Ensure the user can only complete their own tasks
    if (taskToComplete.user_id !== user?.id) {
      alert('You can only complete your own tasks.');
      return;
    }

    await toggleTaskCompletion(taskId);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 text-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">
              Welcome, {user?.email}
            </span>
            <Button
              variant="outline"
              onClick={signOut}
              className="border-gray-300 text-gray-700 hover:bg-gray-100"
            >
              Sign Out
            </Button>
          </div>
        </div>

        <Card className="bg-white border-gray-200 shadow-lg">
          <CardHeader className="flex flex-row items-center justify-between border-b border-gray-200">
            <CardTitle className="text-xl text-gray-800">All Tasks</CardTitle>
            <Button
              onClick={handleCreateTask}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              Create Task
            </Button>
          </CardHeader>
          <CardContent className="pt-6">
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

export default TasksPage;