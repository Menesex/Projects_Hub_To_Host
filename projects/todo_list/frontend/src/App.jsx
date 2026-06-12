import { useState, useEffect } from 'react'
import { getTasks } from './api'
import Sidebar from './components/Sidebar'
import TaskList from './components/TaskList'
import TaskDetail from './components/TaskDetail'

function App() {
  const [tasks, setTasks] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('Tasks')
  const [selectedTaskId, setSelectedTaskId] = useState(null)
  const [loading, setLoading] = useState(true)

  // Derive selectedTask from the tasks array so it's always in sync.
  // When any component calls setTasks(), this updates automatically.
  const selectedTask = tasks.find(t => t.id === selectedTaskId) || null

  useEffect(() => {
    getTasks()
      .then(setTasks)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500 text-sm">Loading your tasks...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-gray-100 text-gray-800">
      <Sidebar
        selectedCategory={selectedCategory}
        onSelectCategory={setSelectedCategory}
      />
      <TaskList
        tasks={tasks}
        setTasks={setTasks}
        category={selectedCategory}
        selectedTask={selectedTask}
        onSelectTask={(task) => setSelectedTaskId(task?.id ?? null)}
      />
      {selectedTask && (
        <TaskDetail
          task={selectedTask}
          setTasks={setTasks}
          setSelectedTask={(task) => setSelectedTaskId(task?.id ?? null)}
        />
      )}
    </div>
  )
}

export default App
