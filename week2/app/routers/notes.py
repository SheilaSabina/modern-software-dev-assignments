from typing import List

from fastapi import APIRouter, HTTPException

from .. import schemas

# Import database dan schemas
from ..services import db

router = APIRouter(prefix="/notes", tags=["notes"])


# --- ENDPOINT 1: AMBIL SEMUA CATATAN (TODO 4) ---
@router.get("", response_model=List[schemas.Note])
def get_notes():
    """
    Mengambil daftar semua catatan yang tersimpan.
    """
    # Kita panggil fungsi list_notes() yang sudah ada di db.py
    notes = db.list_notes()
    return notes


# --- ENDPOINT 2: BUAT CATATAN BARU ---
@router.post("", response_model=schemas.Note)
def create_note(note_in: schemas.NoteCreate):
    """
    Membuat catatan baru.
    """
    # Insert ke DB
    note_id = db.insert_note(note_in.content)

    # Ambil data balik
    note = db.get_note(note_id)
    if not note:
        raise HTTPException(status_code=500, detail="Failed to create note")

    return note


# --- ENDPOINT 3: AMBIL SATU CATATAN ---
@router.get("/{note_id}", response_model=schemas.Note)
def get_single_note(note_id: int):
    """
    Mengambil satu catatan berdasarkan ID.
    """
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return row

# -- FUNGSI DELETE NOTE---
@router.delete("/{note_id}")
def delete_note(note_id: int):
    from ..services.db import get_connection
    with get_connection() as conn:
        cursor = conn.cursor()
        # Hapus action items terkait dulu (karena foreign key)
        cursor.execute("DELETE FROM action_items WHERE note_id = ?", (note_id,))
        # Baru hapus note-nya
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
    return {"status": "success"}
