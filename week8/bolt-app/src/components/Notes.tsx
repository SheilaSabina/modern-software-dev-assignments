import { useState } from 'react';
import { Plus, CreditCard as Edit2, Trash2, Save, X } from 'lucide-react';
import { supabase } from '../lib/supabase';
import type { Note } from '../types/database';

interface NotesProps {
  notes: Note[];
  onUpdate: () => void;
}

export default function Notes({ notes, onUpdate }: NotesProps) {
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState({ title: '', content: '' });

  async function handleCreate() {
    if (!formData.title.trim()) return;

    const { error } = await supabase.from('notes').insert({
      title: formData.title,
      content: formData.content,
    });

    if (!error) {
      setFormData({ title: '', content: '' });
      setIsCreating(false);
      onUpdate();
    }
  }

  async function handleUpdate(id: string) {
    if (!formData.title.trim()) return;

    const { error } = await supabase
      .from('notes')
      .update({
        title: formData.title,
        content: formData.content,
        updated_at: new Date().toISOString(),
      })
      .eq('id', id);

    if (!error) {
      setEditingId(null);
      setFormData({ title: '', content: '' });
      onUpdate();
    }
  }

  async function handleDelete(id: string) {
    const { error } = await supabase.from('notes').delete().eq('id', id);

    if (!error) {
      onUpdate();
    }
  }

  function startEdit(note: Note) {
    setEditingId(note.id);
    setFormData({ title: note.title, content: note.content });
  }

  function cancelEdit() {
    setEditingId(null);
    setIsCreating(false);
    setFormData({ title: '', content: '' });
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Notes</h2>
        <button
          onClick={() => setIsCreating(true)}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus size={20} />
          New Note
        </button>
      </div>

      {isCreating && (
        <div className="bg-white rounded-xl p-6 border border-gray-200 mb-6">
          <input
            type="text"
            placeholder="Note title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full text-xl font-semibold mb-4 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <textarea
            placeholder="Note content"
            value={formData.content}
            onChange={(e) => setFormData({ ...formData, content: e.target.value })}
            className="w-full h-32 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <div className="flex gap-2 mt-4">
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

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {notes.map((note) => (
          <div key={note.id} className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            {editingId === note.id ? (
              <div className="p-6">
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full text-xl font-semibold mb-4 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <textarea
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  className="w-full h-32 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                />
                <div className="flex gap-2 mt-4">
                  <button
                    onClick={() => handleUpdate(note.id)}
                    className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm"
                  >
                    <Save size={16} />
                    Save
                  </button>
                  <button
                    onClick={cancelEdit}
                    className="flex items-center gap-2 bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors text-sm"
                  >
                    <X size={16} />
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <>
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {note.title || 'Untitled'}
                  </h3>
                  <p className="text-gray-600 whitespace-pre-wrap line-clamp-4">
                    {note.content}
                  </p>
                  <p className="text-xs text-gray-400 mt-4">
                    {new Date(note.updated_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 flex gap-2">
                  <button
                    onClick={() => startEdit(note)}
                    className="flex items-center gap-1 text-blue-600 hover:text-blue-700 text-sm"
                  >
                    <Edit2 size={16} />
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(note.id)}
                    className="flex items-center gap-1 text-red-600 hover:text-red-700 text-sm"
                  >
                    <Trash2 size={16} />
                    Delete
                  </button>
                </div>
              </>
            )}
          </div>
        ))}

        {notes.length === 0 && !isCreating && (
          <div className="col-span-full text-center py-12">
            <p className="text-gray-500">No notes yet. Create your first note!</p>
          </div>
        )}
      </div>
    </div>
  );
}
