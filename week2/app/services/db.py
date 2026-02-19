from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


def ensure_data_directory_exists() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    ensure_data_directory_exists()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # Ini penting agar akses kolom pakai nama
    return connection


def init_db() -> None:
    ensure_data_directory_exists()
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );
            """
        )
        connection.commit()


def insert_note(content: str) -> int:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        connection.commit()
        return int(cursor.lastrowid)


def list_notes() -> List[Dict[str, Any]]:
    """Mengambil semua catatan (Refactored untuk return Dict)."""
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
        rows = cursor.fetchall()
        # Konversi ke dictionary agar aman untuk FastAPI
        return [dict(row) for row in rows]


def get_note(note_id: int) -> Optional[Dict[str, Any]]:
    """Mengambil satu catatan (Refactored untuk return Dict)."""
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, content, created_at FROM notes WHERE id = ?",
            (note_id,),
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def insert_action_items(items: list[str], note_id: Optional[int] = None) -> list[int]:
    with get_connection() as connection:
        cursor = connection.cursor()
        ids: list[int] = []
        for item in items:
            cursor.execute(
                "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                (note_id, item),
            )
            ids.append(int(cursor.lastrowid))
        connection.commit()
        return ids
