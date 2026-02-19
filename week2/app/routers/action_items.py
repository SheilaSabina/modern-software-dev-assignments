from typing import List

from fastapi import APIRouter, HTTPException

from .. import schemas

# Import layanan
from ..services import db, extract

# Kita ubah prefix jadi /notes karena action items menempel pada notes
router = APIRouter(prefix="/notes", tags=["action_items"])


# --- FITUR 1: EKSTRAKSI BIASA (REGEX) ---
@router.post("/{note_id}/extract", response_model=List[schemas.ActionItem])
def extract_action_items(note_id: int):
    """
    Ekstraksi menggunakan Regex (Cara Lama).
    """
    note = db.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Panggil fungsi lama di extract.py
    texts = extract.extract_action_items(note["content"])

    # Simpan ke DB
    db.insert_action_items(texts, note_id)

    # Return sesuai format Schema
    return [{"description": t} for t in texts]


# --- FITUR 2: EKSTRAKSI AI (LLM) - TODO 1 & 4 ---
@router.post("/{note_id}/extract-llm", response_model=List[schemas.ActionItem])
def extract_action_items_llm_endpoint(note_id: int):
    """
    Ekstraksi menggunakan AI / Ollama (Cara Baru).
    """
    note = db.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Panggil fungsi LLM di extract.py
    texts = extract.extract_action_items_llm(note["content"])

    # Simpan ke DB
    db.insert_action_items(texts, note_id)

    # Return sesuai format Schema
    return [{"description": t} for t in texts]
