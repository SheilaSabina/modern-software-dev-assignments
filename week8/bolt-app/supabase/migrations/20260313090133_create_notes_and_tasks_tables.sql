/*
  # Developer Control Center Schema

  1. New Tables
    - `notes`
      - `id` (uuid, primary key) - Unique identifier for each note
      - `title` (text) - Note title
      - `content` (text) - Note content/body
      - `created_at` (timestamptz) - When the note was created
      - `updated_at` (timestamptz) - When the note was last updated
    
    - `tasks`
      - `id` (uuid, primary key) - Unique identifier for each task
      - `title` (text) - Task title
      - `description` (text) - Task description
      - `completed` (boolean) - Whether the task is completed
      - `priority` (text) - Task priority (low, medium, high)
      - `due_date` (date) - Task due date
      - `created_at` (timestamptz) - When the task was created
      - `updated_at` (timestamptz) - When the task was last updated

  2. Security
    - Enable RLS on both tables
    - Add policies for authenticated users to perform all operations
*/

CREATE TABLE IF NOT EXISTS notes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL DEFAULT '',
  content text NOT NULL DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL DEFAULT '',
  description text NOT NULL DEFAULT '',
  completed boolean DEFAULT false,
  priority text DEFAULT 'medium',
  due_date date,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all operations on notes"
  ON notes
  FOR ALL
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow all operations on tasks"
  ON tasks
  FOR ALL
  TO authenticated
  USING (true)
  WITH CHECK (true);
