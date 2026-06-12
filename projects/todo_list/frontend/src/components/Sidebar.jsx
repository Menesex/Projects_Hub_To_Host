// LEFT PANEL — category navigation
// Props:
//   selectedCategory (string) — currently active category
//   onSelectCategory (fn)     — called when user clicks a category

import { Sun, Star, Home } from 'lucide-react';

export default function Sidebar({ selectedCategory, onSelectCategory }) {
  // We define our 3 main views
  const menuItems = [
    { name: 'My Day', icon: <Sun size={20} />, color: 'text-orange-500' },
    { name: 'Important', icon: <Star size={20} />, color: 'text-pink-500' },
    { name: 'Tasks', icon: <Home size={20} />, color: 'text-blue-500' },
  ];

  return (
    <aside className="w-64 h-screen bg-gray-50 border-r border-gray-200 p-4 flex flex-col gap-2">
      <h1 className="text-xl font-bold mb-6 px-2 text-gray-800 italic">My Yo-Do</h1>
      
      {menuItems.map((item) => (
        <button
          key={item.name}
          onClick={() => onSelectCategory(item.name)}
          className={`
            flex items-center gap-3 px-3 py-2 rounded-lg transition-colors cursor-pointer
            ${selectedCategory === item.name 
              ? 'bg-blue-100 text-blue-700 font-medium' 
              : 'text-gray-600 hover:bg-gray-200'}
          `}
        >
          <span className={item.color}>{item.icon}</span>
          {item.name}
        </button>
      ))}
    </aside>
  );
}