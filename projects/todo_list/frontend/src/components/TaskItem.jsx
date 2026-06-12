// ONE ROW in the task list
// Props:
//   task (obj)         — the task data
//   isSelected (bool)  — whether this task is currently open in the detail panel
//   onSelect (fn)      — called when the row is clicked
//   onUpdate (fn)      — called to patch the task (toggle complete / important)

import { CheckCircle2, Circle, Star } from 'lucide-react';

export default function TaskItem({ task, isSelected, onSelect, onUpdate }) {
  
  // 1. Handle Toggle Completion
  const toggleComplete = (e) => {
    e.stopPropagation(); // Prevents opening the detail panel when clicking the circle
    onUpdate(task.id, { is_completed: !task.is_completed });
  };

  // 2. Handle Toggle Importance
  const toggleImportant = (e) => {
    e.stopPropagation(); // Prevents opening the detail panel when clicking the star
    onUpdate(task.id, { is_important: !task.is_important });
  };

  return (
    <div 
      onClick={() => onSelect(task)}
      className={`
        group flex items-center gap-4 p-4 mb-2 bg-white rounded-lg shadow-sm border-l-4 cursor-pointer transition-all
        ${isSelected ? 'border-blue-500 bg-blue-50' : 'border-transparent hover:shadow-md'}
      `}
    >
      {/* Checkbox Icon */}
      <button onClick={toggleComplete} className="text-gray-400 hover:text-blue-500 transition-colors">
        {task.is_completed ? <CheckCircle2 className="text-blue-500" /> : <Circle />}
      </button>

      {/* Task Title */}
      <div className="flex-1">
        <p className={`text-sm font-medium ${task.is_completed ? 'line-through text-gray-400' : 'text-gray-700'}`}>
          {task.title}
        </p>
        <p className="text-xs text-gray-400">{task.category}</p>
      </div>

      {/* Star Icon */}
      <button onClick={toggleImportant} className="transition-transform hover:scale-110">
        <Star 
          size={20} 
          className={task.is_important ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300 hover:text-yellow-400'} 
        />
      </button>
    </div>
  );
}