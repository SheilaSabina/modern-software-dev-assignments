from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note, ActionItem
from ..schemas import NoteCreate, NotePatch, NoteRead
from ..services.extract import extract_action_items

router = APIRouter(prefix="/notes", tags=["notes"])


def _handle_action_items(note_id: int, content: str, db: Session) -> None:
    """Background task to extract and save action items for a note."""
    try:
        # Delete existing action items for this note
        db.query(ActionItem).filter(ActionItem.note_id == note_id).delete()
        
        # Extract new action items and save them
        action_texts = extract_action_items(content)
        for text in action_texts:
            action_item = ActionItem(note_id=note_id, text=text)
            db.add(action_item)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Note, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Note, sort_field)))
    else:
        stmt = stmt.order_by(desc(Note.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks()) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    db.commit()
    
    # Add background task to extract action items
    background_tasks.add_task(_handle_action_items, note.id, note.content, db)
    
    return NoteRead.model_validate(note)


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NotePatch, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks()) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    db.commit()
    
    # Add background task to extract action items
    background_tasks.add_task(_handle_action_items, note.id, note.content, db)
    
    return NoteRead.model_validate(note)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)