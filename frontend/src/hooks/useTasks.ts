import { useState, useEffect } from 'react';
import { apiClient } from '@/src/app/api/client';
import { Task } from '@/src/lib/types';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch tasks
  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<Task[]>('/tasks');

      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setTasks(response.data);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  // Create a new task
  const createTask = async (taskData: { title: string; description?: string; status?: string }) => {
    try {
      setLoading(true);
      const response = await apiClient.post<{ task: Task }>('/tasks', {
        ...taskData,
        status: taskData.status || 'pending'
      });

      if (response.error) {
        setError(response.error);
        return null;
      } else if (response.data) {
        // Refresh the task list to ensure we have the latest data
        await fetchTasks();
        return response.data.task;
      }
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Update an existing task
  const updateTask = async (taskId: string, taskData: Partial<Task>) => {
    try {
      setLoading(true);
      const response = await apiClient.put<{ task: Task }>(`/tasks/${taskId}`, taskData);

      if (response.error) {
        setError(response.error);
        return null;
      } else if (response.data) {
        setTasks(tasks.map(task =>
          task.id === taskId ? response.data.task : task
        ));
        return response.data.task;
      }
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Delete a task
  const deleteTask = async (taskId: string) => {
    try {
      setLoading(true);
      const response = await apiClient.delete(`/tasks/${taskId}`);

      if (response.error) {
        setError(response.error);
        return false;
      } else {
        setTasks(tasks.filter(task => task.id !== taskId));
        return true;
      }
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Toggle task completion status
  const toggleTaskCompletion = async (taskId: string) => {
    try {
      const task = tasks.find(t => t.id === taskId);
      if (!task) return null;

      const newStatus = task.status === 'completed' ? 'pending' : 'completed';
      return await updateTask(taskId, { status: newStatus });
    } catch (err: any) {
      setError(err.message || 'Failed to toggle task completion');
      return null;
    }
  };

  // Load tasks when hook is initialized
  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
};