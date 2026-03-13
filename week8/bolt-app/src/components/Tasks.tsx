import { useState } from 'react';
import { Plus, CreditCard as Edit2, Trash2, Save, X, CheckCircle2, Circle } from 'lucide-react';
import { supabase } from '../lib/supabase';
import type { Task } from '../types/database';

interface TasksProps {
  tasks: Task[];
  onUpdate: () => void;
}

export default function Tasks({ tasks, onUpdate }: TasksProps) {
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium',
    due_date: '',
  });

  async function handleCreate() {
    if (!formData.title.trim()) return;

    const { error } = await supabase.from('tasks').insert({
      title: formData.title,
      description: formData.description,
      priority: formData.priority,
      due_date: formData.due_date || null,
    });

    if (!error) {
      setFormData({ title: '', description: '', priority: 'medium', due_date: '' });
      setIsCreating(false);
      onUpdate();
    }
  }

  async function handleUpdate(id: string) {
    if (!formData.title.trim()) return;

    const { error } = await supabase
      .from('tasks')
      .update({
        title: formData.title,
        description: formData.description,
        priority: formData.priority,
        due_date: formData.due_date || null,
        updated_at: new Date().toISOString(),
      })
      .eq('id', id);

    if (!error) {
      setEditingId(null);
      setFormData({ title: '', description: '', priority: 'medium', due_date: '' });
      onUpdate();
    }
  }

  async function handleDelete(id: string) {
    const { error } = await supabase.from('tasks').delete().eq('id', id);

    if (!error) {
      onUpdate();
    }
  }

  async function toggleComplete(task: Task) {
    const { error } = await supabase
      .from('tasks')
      .update({ completed: !task.completed })
      .eq('id', task.id);

    if (!error) {
      onUpdate();
    }
  }

  function startEdit(task: Task) {
    setEditingId(task.id);
    setFormData({
      title: task.title,
      description: task.description,
      priority: task.priority,
      due_date: task.due_date || '',
    });
  }

  function cancelEdit() {
    setEditingId(null);
    setIsCreating(false);
    setFormData({ title: '', description: '', priority: 'medium', due_date: '' });
  }

  const activeTasks = tasks.filter(t => !t.completed);
  const completedTasks = tasks.filter(t => t.completed);

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Tasks</h2>
        <button
          onClick={() => setIsCreating(true)}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus size={20} />
          New Task
        </button>
      </div>

      {isCreating && (
        <div className="bg-white rounded-xl p-6 border border-gray-200 mb-6">
          <input
            type="text"
            placeholder="Task title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full text-xl font-semibold mb-4 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <textarea
            placeholder="Task description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="w-full h-24 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none mb-4"
          />
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Due Date</label>
              <input
                type="date"
                value={formData.due_date}
                onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleCreate}
              className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              <Save size={18} />
              Save
            </button>
            <button
              onClick={cancelEdit}
              className="flex items-center gap-2 bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors"
            >
              <X size={18} />
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Active Tasks ({activeTasks.length})</h3>
          <div className="space-y-3">
            {activeTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                editingId={editingId}
                formData={formData}
                onToggleComplete={toggleComplete}
                onStartEdit={startEdit}
                onUpdate={handleUpdate}
                onDelete={handleDelete}
                onCancel={cancelEdit}
                onFormChange={setFormData}
              />
            ))}
            {activeTasks.length === 0 && (
              <p className="text-gray-500 text-sm">No active tasks</p>
            )}
          </div>
        </div>

        {completedTasks.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Completed ({completedTasks.length})</h3>
            <div className="space-y-3">
              {completedTasks.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  editingId={editingId}
                  formData={formData}
                  onToggleComplete={toggleComplete}
                  onStartEdit={startEdit}
                  onUpdate={handleUpdate}
                  onDelete={handleDelete}
                  onCancel={cancelEdit}
                  onFormChange={setFormData}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

interface TaskItemProps {
  task: Task;
  editingId: string | null;
  formData: { title: string; description: string; priority: string; due_date: string };
  onToggleComplete: (task: Task) => void;
  onStartEdit: (task: Task) => void;
  onUpdate: (id: string) => void;
  onDelete: (id: string) => void;
  onCancel: () => void;
  onFormChange: (data: any) => void;
}

function TaskItem({
  task,
  editingId,
  formData,
  onToggleComplete,
  onStartEdit,
  onUpdate,
  onDelete,
  onCancel,
  onFormChange,
}: TaskItemProps) {
  if (editingId === task.id) {
    return (
      <div className="bg-white rounded-lg p-6 border border-gray-200">
        <input
          type="text"
          value={formData.title}
          onChange={(e) => onFormChange({ ...formData, title: e.target.value })}
          className="w-full text-lg font-semibold mb-4 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <textarea
          value={formData.description}
          onChange={(e) => onFormChange({ ...formData, description: e.target.value })}
          className="w-full h-24 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none mb-4"
        />
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
            <select
              value={formData.priority}
              onChange={(e) => onFormChange({ ...formData, priority: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Due Date</label>
            <input
              type="date"
              value={formData.due_date}
              onChange={(e) => onFormChange({ ...formData, due_date: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => onUpdate(task.id)}
            className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm"
          >
            <Save size={16} />
            Save
          </button>
          <button
            onClick={onCancel}
            className="flex items-center gap-2 bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors text-sm"
          >
            <X size={16} />
            Cancel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg p-4 border border-gray-200 flex items-start gap-4 ${
      task.completed ? 'opacity-60' : ''
    }`}>
      <button
        onClick={() => onToggleComplete(task)}
        className="mt-1 text-gray-400 hover:text-green-600 transition-colors"
      >
        {task.completed ? <CheckCircle2 size={24} className="text-green-600" /> : <Circle size={24} />}
      </button>

      <div className="flex-1">
        <h4 className={`font-semibold text-gray-900 mb-1 ${task.completed ? 'line-through' : ''}`}>
          {task.title}
        </h4>
        {task.description && (
          <p className="text-gray-600 text-sm mb-3">{task.description}</p>
        )}
        <div className="flex items-center gap-3">
          <span className={`text-xs px-2 py-1 rounded-full ${
            task.priority === 'high' ? 'bg-red-100 text-red-700' :
            task.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
            'bg-gray-100 text-gray-700'
          }`}>
            {task.priority}
          </span>
          {task.due_date && (
            <span className="text-xs text-gray-500">{new Date(task.due_date).toLocaleDateString()}</span>
          )}
        </div>
      </div>

      <div className="flex gap-2">
        <button
          onClick={() => onStartEdit(task)}
          className="text-blue-600 hover:text-blue-700"
        >
          <Edit2 size={18} />
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="text-red-600 hover:text-red-700"
        >
          <Trash2 size={18} />
        </button>
      </div>
    </div>
  );
}
