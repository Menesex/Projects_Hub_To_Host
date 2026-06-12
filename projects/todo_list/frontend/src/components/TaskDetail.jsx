import { useState } from 'react';
import { X, Trash2, Plus, Calendar, CheckCircle2, Circle } from 'lucide-react';
import { updateTask, deleteTask, createStep, updateStep, deleteStep } from '../api';

export default function TaskDetail({ task, setTasks, setSelectedTask }) {
  const [stepTitle, setStepTitle] = useState("");

  if (!task) return null;

  // 1. Update Task Fields (Title, Description, Due Date)
  const handleBlurUpdate = async (field, value) => {
    if (task[field] === value) return;
    const updated = await updateTask(task.id, { [field]: value });
    // setTasks update is enough — App derives selectedTask from tasks automatically
    setTasks(prev => prev.map(t => t.id === task.id ? { ...t, ...updated } : t));
  };

  // 2. Steps Logic (Add, Toggle, Delete) — optimistic updates (UI first, API in background)
  const handleAddStep = (e) => {
    if (e.key !== 'Enter' || !stepTitle.trim()) return;
    const tempStep = { id: `temp-${Date.now()}`, title: stepTitle, is_completed: false, task_id: task.id };
    setTasks(prev => prev.map(t =>
      t.id === task.id ? { ...t, steps: [...(t.steps || []), tempStep] } : t
    ));
    setStepTitle("");
    // Save to DB in background, replace temp step with real one when done
    createStep(task.id, { title: tempStep.title }).then(realStep => {
      setTasks(prev => prev.map(t =>
        t.id === task.id
          ? { ...t, steps: t.steps.map(s => s.id === tempStep.id ? realStep : s) }
          : t
      ));
    });
  };

  const handleToggleStep = (stepId, currentStatus) => {
    // Update UI instantly
    setTasks(prev => prev.map(t =>
      t.id === task.id
        ? { ...t, steps: t.steps.map(s => s.id === stepId ? { ...s, is_completed: !currentStatus } : s) }
        : t
    ));
    // Sync with DB in background
    updateStep(stepId, !currentStatus);
  };

  const handleDeleteStep = (stepId) => {
    // Remove from UI instantly
    setTasks(prev => prev.map(t =>
      t.id === task.id
        ? { ...t, steps: t.steps.filter(s => s.id !== stepId) }
        : t
    ));
    // Delete from DB in background
    deleteStep(stepId);
  };

  // 3. Delete Task
  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      await deleteTask(task.id);
      setTasks(prev => prev.filter(t => t.id !== task.id));
      setSelectedTask(null); // close the panel
    }
  };

  return (
    <aside className="w-96 h-screen bg-white border-l border-gray-200 p-6 flex flex-col shadow-2xl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <span className="text-xs font-bold text-blue-500 uppercase tracking-wider">Task Details</span>
        <button onClick={() => setSelectedTask(null)} className="p-1 hover:bg-gray-100 rounded-full cursor-pointer">
          <X size={20} />
        </button>
      </div>

      {/* Title */}
      <input
        key={`title-${task.id}`}
        className="text-xl font-bold text-gray-800 outline-none mb-6 border-b border-transparent focus:border-gray-100 w-full"
        defaultValue={task.title}
        onBlur={(e) => handleBlurUpdate('title', e.target.value)}
      />

      <div className="flex-1 overflow-y-auto space-y-8">
        {/* Steps Section */}
        <div>
          <h4 className="text-xs font-semibold text-gray-400 mb-3 uppercase tracking-widest">Steps</h4>
          <div className="space-y-1">
            {task.steps?.map(step => (
              <div key={step.id} className="group flex items-center gap-3 p-2 hover:bg-gray-50 rounded transition-colors">
                <button
                  onClick={() => handleToggleStep(step.id, step.is_completed)}
                  className="text-gray-400 hover:text-blue-500 cursor-pointer"
                >
                  {step.is_completed ? <CheckCircle2 size={18} className="text-blue-500" /> : <Circle size={18} />}
                </button>
                <span className={`text-sm flex-1 ${step.is_completed ? 'line-through text-gray-400' : 'text-gray-700'}`}>
                  {step.title}
                </span>
                <button
                  onClick={() => handleDeleteStep(step.id)}
                  className="opacity-0 group-hover:opacity-100 text-gray-300 hover:text-red-500 transition-opacity cursor-pointer"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))}
          </div>

          <div className="flex items-center gap-3 p-2 mt-2 border-t border-gray-100">
            <Plus size={16} className="text-blue-500" />
            <input
              placeholder="Add step"
              className="text-sm outline-none w-full bg-transparent"
              value={stepTitle}
              onChange={(e) => setStepTitle(e.target.value)}
              onKeyDown={handleAddStep}
            />
          </div>
        </div>

        {/* Due Date Section */}
        <div>
          <label className="flex items-center gap-2 text-xs font-semibold text-gray-400 mb-2 uppercase tracking-widest">
            <Calendar size={14} /> Due Date
          </label>
          <input
            key={`date-${task.id}`}
            type="date"
            className="w-full p-2 bg-gray-50 rounded border border-gray-100 text-sm outline-none focus:border-blue-300"
            defaultValue={task.due_date ? task.due_date.split('T')[0] : ""}
            onChange={(e) => handleBlurUpdate('due_date', e.target.value)}
          />
        </div>

        {/* Description Section */}
        <div>
          <label className="text-xs font-semibold text-gray-400 block mb-2 uppercase tracking-widest">Description</label>
          <textarea
            key={`desc-${task.id}`}
            className="w-full h-32 p-3 bg-gray-50 rounded border border-gray-100 text-sm outline-none focus:ring-1 ring-blue-100 resize-none"
            placeholder="Add a note..."
            defaultValue={task.description}
            onBlur={(e) => handleBlurUpdate('description', e.target.value)}
          />
        </div>
      </div>

      {/* Delete Footer */}
      <button
        onClick={handleDelete}
        className="mt-6 flex items-center justify-center gap-2 text-red-400 p-3 hover:bg-red-50 hover:text-red-600 rounded-lg transition-all cursor-pointer"
      >
        <Trash2 size={18} />
        <span className="text-sm font-semibold">Delete Task</span>
      </button>
    </aside>
  );
}
