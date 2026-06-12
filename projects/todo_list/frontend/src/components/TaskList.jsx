// MIDDLE PANEL — list of tasks for the selected category
// Props:
//   tasks (array)        — all tasks from the API
//   setTasks (fn)        — update tasks state in App
//   category (string)    — current filter ("Tasks", "Important", "My Day")
//   selectedTask (obj)   — currently open task
//   onSelectTask (fn)    — called when user clicks a task row

import { useState } from 'react';
import TaskItem from './TaskItem';
import { Plus } from 'lucide-react';
import { createTask, updateTask } from '../api';

export default function TaskList({ tasks, setTasks, category, selectedTask, onSelectTask }) {
  const [newTaskTitle, setNewTaskTitle] = useState("");

  // 1. FILTERING LOGIC
  const filteredTasks = tasks.filter(task => {
    if (category === "Important") return task.is_important;
    if (category === "My Day") {
        const today = new Date().toISOString().split('T')[0];
        return task.created_at.startsWith(today);
    }
    return true; // "Tasks" shows everything
  });

  // 2. CREATE NEW TASK
  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    const newTask = await createTask({
      title: newTaskTitle,
      category: category === "Tasks" ? "Tasks" : category,
      is_important: category === "Important"
    });

    setTasks([...tasks, newTask]); // Add the new task to the screen immediately
    setNewTaskTitle(""); // Clear the input
  };

  // 3. UPDATE TASK (Used by TaskItem)
  const handleUpdate = (taskId, updates) => {
    // Update UI instantly so it feels responsive
    setTasks(prev => prev.map(t => t.id === taskId ? { ...t, ...updates } : t));
    // Persist the change to the database
    updateTask(taskId, updates);
  };

  return (
    <main className="flex-1 p-8 bg-gray-100 overflow-y-auto">
      <header className="mb-8">
        <h2 className="text-2xl font-bold text-blue-600">{category}</h2>
      </header>

      <div className="max-w-3xl">
        {filteredTasks.map(task => (
          <TaskItem 
            key={task.id} 
            task={task} 
            isSelected={selectedTask?.id === task.id}
            onSelect={onSelectTask}
            onUpdate={handleUpdate}
          />
        ))}

        {/* Create Task Input */}
        <form onSubmit={handleCreate} className="mt-6 flex items-center gap-3 bg-white p-4 rounded-lg shadow-sm">
          <Plus className="text-blue-500" />
          <input 
            type="text"
            placeholder="Add a task"
            className="flex-1 outline-none text-sm"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
          />
          <button type="submit" className="text-blue-500 font-medium text-sm px-4 py-1 hover:bg-blue-50 rounded">
            Add
          </button>
        </form>
      </div>
    </main>
  );
}