export interface Database {
  public: {
    Tables: {
      notes: {
        Row: {
          id: string;
          title: string;
          content: string;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          title?: string;
          content?: string;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          title?: string;
          content?: string;
          created_at?: string;
          updated_at?: string;
        };
      };
      tasks: {
        Row: {
          id: string;
          title: string;
          description: string;
          completed: boolean;
          priority: string;
          due_date: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          title?: string;
          description?: string;
          completed?: boolean;
          priority?: string;
          due_date?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          title?: string;
          description?: string;
          completed?: boolean;
          priority?: string;
          due_date?: string | null;
          created_at?: string;
          updated_at?: string;
        };
      };
    };
  };
}

export type Note = Database['public']['Tables']['notes']['Row'];
export type Task = Database['public']['Tables']['tasks']['Row'];
