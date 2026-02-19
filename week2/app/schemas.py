from typing import List, Optional

from pydantic import BaseModel


# --- 1. Action Items (Tugas) ---
class ActionItemBase(BaseModel):
    description: str


class ActionItemCreate(ActionItemBase):
    pass


class ActionItem(ActionItemBase):
    class Config:
        from_attributes = True


# --- 2. Notes (Catatan) ---
class NoteBase(BaseModel):
    content: str  # <-- KITA UBAH JADI 'content' AGAR SESUAI DB


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    created_at: Optional[str] = None
    # Kita buat action_items opsional dulu agar tidak error saat load awal
    action_items: List[ActionItem] = []

    class Config:
        from_attributes = True
