import React from 'react';
import { Task } from '@/src/lib/types';
import TaskItem from '@/src/components/tasks/TaskItem';

interface TaskListProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onComplete: (taskId: string, completed: boolean) => void;
  loading?: boolean;
}

const TaskList: React.FC<TaskListProps> = ({ tasks = [], onEdit, onDelete, onComplete, loading = false }) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Filter out any undefined or null tasks before rendering
  const validTasks = tasks.filter(task => task && task.id);

  if (validTasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No tasks found. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {validTasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onEdit={() => onEdit(task)}
          onDelete={() => onDelete(task.id)}
          onComplete={(completed) => onComplete(task.id, completed)}
        />
      ))}
    </div>
  );
};

export default TaskList;