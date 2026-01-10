import React from 'react';
import { Task } from '@/src/lib/types';
import { Card, CardContent, CardFooter } from '@/src/components/ui/Card';
import { Button } from '@/src/components/ui/Button';

interface TaskItemProps {
  task: Task;
  onEdit: () => void;
  onDelete: () => void;
  onComplete: (completed: boolean) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onEdit, onDelete, onComplete }) => {
  const handleToggleComplete = () => {
    const newStatus = task.status === 'completed' ? 'pending' : 'completed';
    onComplete(newStatus === 'completed');
  };

  return (
    <Card className={`transition-all duration-200 ${task.status === 'completed' ? 'bg-gray-100 border-gray-200' : 'bg-white border-gray-200'}`}>
      <CardContent className="pt-6">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div className="flex items-start space-x-3">
            <input
              type="checkbox"
              checked={task.status === 'completed'}
              onChange={handleToggleComplete}
              className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <div>
              <h3 className={`text-lg font-medium ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 text-sm ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-900 font-medium'}`}>
                  {task.description}
                </p>
              )}
              <div className="mt-2 flex flex-wrap items-center text-xs text-gray-500">
                <span>Status: {task.status.replace('-', ' ')}</span>
                <span className="mx-2 hidden sm:inline">•</span>
                <span className="block sm:inline mt-1 sm:mt-0">Created: {new Date(task.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-2 bg-gray-50 rounded-b-lg p-4 border-t border-gray-200">
        <Button
          variant={task.status === 'completed' ? 'secondary' : 'outline'}
          size="sm"
          onClick={handleToggleComplete}
          className="w-full sm:w-auto"
        >
          {task.status === 'completed' ? 'Mark Pending' : 'Complete'}
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={onEdit}
          className="w-full sm:w-auto"
        >
          Edit
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={onDelete}
          className="w-full sm:w-auto"
        >
          Delete
        </Button>
      </CardFooter>
    </Card>
  );
};

export default TaskItem;