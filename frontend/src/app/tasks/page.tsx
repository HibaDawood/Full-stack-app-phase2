'use client';

import { useState, useEffect } from 'react';
import { tasksAPI, Task } from '../api/client';
import TaskItem from '@/src/components/tasks/TaskItem';
import TaskModal from '@/src/components/tasks/TaskModal';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [newTaskStatus, setNewTaskStatus] = useState<'pending' | 'in-progress' | 'completed'>('pending');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  // ---------------- FETCH TASKS ----------------
  const fetchTasks = async () => {
    try {
      setLoading(true);
      const fetchedTasks = await tasksAPI.getTasks();

      // 🔒 SAFETY: tasks are properly typed
      const safeTasks = fetchedTasks;

      setTasks(safeTasks);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  // ---------------- CREATE TASK ----------------
  const createTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      setError('Task title is required');
      return;
    }

    try {
      const newTask = await tasksAPI.createTask({
        title: newTaskTitle,
        description: newTaskDescription,
        status: newTaskStatus,
      });

      setTasks([...tasks, newTask]);
      setNewTaskTitle('');
      setNewTaskDescription('');
      setNewTaskStatus('pending'); // Reset to default
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
    }
  };

  // ---------------- TOGGLE TASK ----------------
  const toggleTaskCompletion = async (taskId: string, intendedStatus: 'pending' | 'completed') => {
    // Use the intended status directly
    const newStatus = intendedStatus;

    try {
      const updatedTask = await tasksAPI.updateTask(taskId, { status: newStatus });
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    }
  };

  // ---------------- DELETE TASK ----------------
  const deleteTask = async (taskId: string) => {
    try {
      await tasksAPI.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
    }
  };

  // ---------------- EDIT TASK ----------------
  const startEditing = (task: Task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const saveEdit = async (taskData: { title: string; description?: string; status: 'pending' | 'in-progress' | 'completed' }) => {
    if (!editingTask) return;

    try {
      const updatedTask = await tasksAPI.updateTask(editingTask.id, {
        title: taskData.title,
        description: taskData.description,
        status: taskData.status,
      });

      setTasks(tasks.map(task =>
        task.id === editingTask.id
          ? updatedTask
          : task
      ));

      cancelEdit();
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    }
  };

  const cancelEdit = () => {
    setEditingTask(null);
    setIsModalOpen(false);
  };

  // ---------------- FILTERS ----------------
  const pendingTasks = tasks.filter(task => task.status === 'pending');
  const inProgressTasks = tasks.filter(task => task.status === 'in-progress');
  const completedTasks = tasks.filter(task => task.status === 'completed');

  const filterTasks = (list: Task[]) =>
    list.filter(task =>
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (task.description &&
        task.description.toLowerCase().includes(searchTerm.toLowerCase()))
    );

  const filteredPendingTasks = filterTasks(pendingTasks);
  const filteredInProgressTasks = filterTasks(inProgressTasks);
  const filteredCompletedTasks = filterTasks(completedTasks);

  if (loading) {
    return <div className="p-10 text-center">Loading tasks...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-6 text-center text-3xl font-bold">Your Tasks</h1>

        {error && (
          <div className="mb-4 rounded bg-red-100 p-3 text-red-600">
            {error}
          </div>
        )}

        {/* SEARCH */}
        <input
          type="text"
          placeholder="Search tasks..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          className="mb-4 w-full rounded border p-2"
        />

        {/* ADD TASK */}
        <form onSubmit={createTask} className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-2">
          <input
            value={newTaskTitle}
            onChange={e => setNewTaskTitle(e.target.value)}
            placeholder="Task title"
            className="md:col-span-2 rounded border p-2"
          />
          <input
            value={newTaskDescription}
            onChange={e => setNewTaskDescription(e.target.value)}
            placeholder="Description"
            className="rounded border p-2"
          />
          <select
            value={newTaskStatus}
            onChange={e => setNewTaskStatus(e.target.value as 'pending' | 'in-progress' | 'completed')}
            className="rounded border p-2"
          >
            <option value="pending">Pending</option>
            <option value="in-progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
          <button className="md:col-span-4 rounded bg-indigo-600 px-4 py-2 text-white">
            Add Task
          </button>
        </form>

        {/* PENDING */}
        <h2 className="mb-2 text-xl font-semibold">
          Pending ({filteredPendingTasks.length})
        </h2>

        {filteredPendingTasks.map(task => (
          <TaskItem
            key={task.id}
            task={task}
            onEdit={() => startEditing(task)}
            onDelete={() => deleteTask(task.id)}
            onComplete={(completed: boolean) => toggleTaskCompletion(task.id, completed ? 'completed' : 'pending')}
          />
        ))}

        {/* IN PROGRESS */}
        <h2 className="mt-8 mb-2 text-xl font-semibold">
          In Progress ({filteredInProgressTasks.length})
        </h2>

        {filteredInProgressTasks.map(task => (
          <TaskItem
            key={task.id}
            task={task}
            onEdit={() => startEditing(task)}
            onDelete={() => deleteTask(task.id)}
            onComplete={(completed: boolean) => toggleTaskCompletion(task.id, completed ? 'completed' : 'pending')}
          />
        ))}

        {/* COMPLETED */}
        <h2 className="mt-8 mb-2 text-xl font-semibold">
          Completed ({filteredCompletedTasks.length})
        </h2>

        {filteredCompletedTasks.map(task => (
          <TaskItem
            key={task.id}
            task={task}
            onEdit={() => startEditing(task)}
            onDelete={() => deleteTask(task.id)}
            onComplete={(completed: boolean) => toggleTaskCompletion(task.id, completed ? 'completed' : 'pending')}
          />
        ))}
      </div>

      {/* Task Modal */}
      <TaskModal
        isOpen={isModalOpen}
        onClose={cancelEdit}
        task={editingTask}
        onSave={saveEdit}
      />
    </div>
  );
}
