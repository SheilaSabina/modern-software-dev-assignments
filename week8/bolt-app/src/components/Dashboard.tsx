import { useState, useEffect } from 'react';
import { LayoutDashboard, StickyNote, CheckSquare } from 'lucide-react';
import { supabase } from '../lib/supabase';
import type { Note, Task } from '../types/database';
import Overview from './Overview';
import Notes from './Notes';
import Tasks from './Tasks';

type View = 'overview' | 'notes' | 'tasks';

export default function Dashboard() {
  const [currentView, setCurrentView] = useState<View>('overview');
  const [notes, setNotes] = useState<Note[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    setLoading(true);

    const [notesResult, tasksResult] = await Promise.all([
      supabase.from('notes').select('*').order('updated_at', { ascending: false }),
      supabase.from('tasks').select('*').order('created_at', { ascending: false })
    ]);

    if (notesResult.data) setNotes(notesResult.data);
    if (tasksResult.data) setTasks(tasksResult.data);

    setLoading(false);
  }

  const navItems = [
    { id: 'overview' as View, label: 'Overview', icon: LayoutDashboard },
    { id: 'notes' as View, label: 'Notes', icon: StickyNote },
    { id: 'tasks' as View, label: 'Tasks', icon: CheckSquare },
  ];

  return (
    <div className="flex h-screen bg-gray-50">
      <aside className="w-64 bg-white border-r border-gray-200">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-900">Dev Control</h1>
          <p className="text-sm text-gray-500 mt-1">Dashboard</p>
        </div>

        <nav className="px-3">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentView === item.id;

            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg mb-1 transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>

      <main className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto p-8">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-gray-500">Loading...</div>
            </div>
          ) : (
            <>
              {currentView === 'overview' && (
                <Overview notes={notes} tasks={tasks} />
              )}
              {currentView === 'notes' && (
                <Notes notes={notes} onUpdate={fetchData} />
              )}
              {currentView === 'tasks' && (
                <Tasks tasks={tasks} onUpdate={fetchData} />
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}
