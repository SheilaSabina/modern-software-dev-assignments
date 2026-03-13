import { StickyNote, CheckSquare, Clock, CheckCircle2 } from 'lucide-react';
import type { Note, Task } from '../types/database';

interface OverviewProps {
  notes: Note[];
  tasks: Task[];
}

export default function Overview({ notes, tasks }: OverviewProps) {
  const completedTasks = tasks.filter(t => t.completed).length;
  const pendingTasks = tasks.filter(t => !t.completed).length;
  const recentNotes = notes.slice(0, 5);
  const recentTasks = tasks.slice(0, 5);

  const stats = [
    {
      label: 'Total Notes',
      value: notes.length,
      icon: StickyNote,
      color: 'bg-blue-100 text-blue-600',
    },
    {
      label: 'Total Tasks',
      value: tasks.length,
      icon: CheckSquare,
      color: 'bg-green-100 text-green-600',
    },
    {
      label: 'Completed',
      value: completedTasks,
      icon: CheckCircle2,
      color: 'bg-emerald-100 text-emerald-600',
    },
    {
      label: 'Pending',
      value: pendingTasks,
      icon: Clock,
      color: 'bg-orange-100 text-orange-600',
    },
  ];

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-900 mb-8">Overview</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.label} className="bg-white rounded-xl p-6 border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon size={24} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Notes</h3>
          {recentNotes.length === 0 ? (
            <p className="text-gray-500 text-sm">No notes yet</p>
          ) : (
            <div className="space-y-3">
              {recentNotes.map((note) => (
                <div key={note.id} className="border-l-4 border-blue-500 pl-3 py-2">
                  <h4 className="font-medium text-gray-900">{note.title || 'Untitled'}</h4>
                  <p className="text-sm text-gray-500 line-clamp-2">{note.content}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Tasks</h3>
          {recentTasks.length === 0 ? (
            <p className="text-gray-500 text-sm">No tasks yet</p>
          ) : (
            <div className="space-y-3">
              {recentTasks.map((task) => (
                <div key={task.id} className="flex items-start gap-3">
                  <div className={`mt-1 ${task.completed ? 'text-green-500' : 'text-gray-400'}`}>
                    <CheckCircle2 size={18} />
                  </div>
                  <div className="flex-1">
                    <h4 className={`font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                      {task.title}
                    </h4>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        task.priority === 'high' ? 'bg-red-100 text-red-700' :
                        task.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-gray-100 text-gray-700'
                      }`}>
                        {task.priority}
                      </span>
                      {task.due_date && (
                        <span className="text-xs text-gray-500">{task.due_date}</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
