from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)')
    conn.close()

@app.route('/notes', methods=['GET', 'POST'])
def handle_notes():
    conn = sqlite3.connect('database.db')
    if request.method == 'POST':
        data = request.json
        conn.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (data['title'], data['content']))
        conn.commit()
        return jsonify({"message": "Note created"}), 201
    
    cursor = conn.execute('SELECT * FROM notes')
    notes = [{"id": row[0], "title": row[1], "content": row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(notes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)