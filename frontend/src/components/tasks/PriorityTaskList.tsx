import React from 'react';
import { Task } from '@/lib/types';
import TaskItem from '@/components/tasks/TaskItem';
import { useLanguage } from '@/contexts/LanguageContext';

interface PriorityTaskListProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onComplete: (taskId: string, completed: boolean) => void;
  loading?: boolean;
}

const PriorityTaskList: React.FC<PriorityTaskListProps> = ({
  tasks = [],
  onEdit,
  onDelete,
  onComplete,
  loading = false
}) => {
  const { t } = useLanguage();

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Filter out any undefined or null tasks before organizing
  const validTasks = tasks.filter(task => task && task.id);

  // Organize tasks by status
  const pendingTasks = validTasks.filter(task => task.status === 'pending');
  const inProgressTasks = validTasks.filter(task => task.status === 'in-progress');
  const completedTasks = validTasks.filter(task => task.status === 'completed');

  if (validTasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">{t('noTasks')}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Pending Tasks Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-yellow-600 mb-4 flex items-center">
          <span className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></span>
          {t('pendingTasks')}
        </h2>
        {pendingTasks.length === 0 ? (
          <p className="text-gray-500 text-center py-4">{t('noPending')}</p>
        ) : (
          <div className="space-y-3">
            {pendingTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onEdit={() => onEdit(task)}
                onDelete={() => onDelete(task.id)}
                onComplete={(completed) => onComplete(task.id, completed)}
              />
            ))}
          </div>
        )}
      </div>

      {/* In Progress Tasks Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-blue-600 mb-4 flex items-center">
          <span className="w-3 h-3 bg-blue-500 rounded-full mr-2"></span>
          {t('inProgress')}
        </h2>
        {inProgressTasks.length === 0 ? (
          <p className="text-gray-500 text-center py-4">{t('noInProgress')}</p>
        ) : (
          <div className="space-y-3">
            {inProgressTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onEdit={() => onEdit(task)}
                onDelete={() => onDelete(task.id)}
                onComplete={(completed) => onComplete(task.id, completed)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Completed Tasks Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-green-600 mb-4 flex items-center">
          <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
          {t('completedTasks')}
        </h2>
        {completedTasks.length === 0 ? (
          <p className="text-gray-500 text-center py-4">{t('noCompleted')}</p>
        ) : (
          <div className="space-y-3">
            {completedTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onEdit={() => onEdit(task)}
                onDelete={() => onDelete(task.id)}
                onComplete={(completed) => onComplete(task.id, completed)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PriorityTaskList;