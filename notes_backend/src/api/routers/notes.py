from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from src.api.db import fetch_all, fetch_one, execute, execute_returning
from src.api.models import NoteCreate, NoteUpdate, NoteOut

router = APIRouter(prefix="/notes", tags=["Notes"])


def _row_to_note_out(row: dict) -> NoteOut:
    # Map DB row dict to NoteOut model
    return NoteOut(
        id=row["id"],
        title=row["title"],
        content=row["content"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.get(
    "",
    response_model=List[NoteOut],
    summary="List notes",
    description="Retrieve all notes, optionally filtered by a case-insensitive search on title or content.",
)
def list_notes(search: Optional[str] = Query(None, description="Search string to filter notes by title/content")):
    """List all notes with optional text search."""
    if search:
        q = """
            SELECT id, title, content, created_at, updated_at
            FROM notes
            WHERE title ILIKE %s OR content ILIKE %s
            ORDER BY updated_at DESC, created_at DESC
        """
        like = f"%{search}%"
        rows = fetch_all(q, [like, like])
    else:
        q = """
            SELECT id, title, content, created_at, updated_at
            FROM notes
            ORDER BY updated_at DESC, created_at DESC
        """
        rows = fetch_all(q)
    return [_row_to_note_out(r) for r in rows]


@router.post(
    "",
    response_model=NoteOut,
    status_code=201,
    summary="Create note",
    description="Create a new note with title and content.",
)
def create_note(payload: NoteCreate):
    """Create a new note and return it."""
    q = """
        INSERT INTO notes (title, content)
        VALUES (%s, %s)
        RETURNING id, title, content, created_at, updated_at
    """
    row = execute_returning(q, [payload.title, payload.content])
    if not row:
        raise HTTPException(status_code=500, detail="Failed to create note")
    return _row_to_note_out(row)


@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get note",
    description="Retrieve a single note by ID.",
)
def get_note(note_id: int):
    """Get note by id."""
    q = """
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE id = %s
    """
    row = fetch_one(q, [note_id])
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    return _row_to_note_out(row)


@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update note",
    description="Update title and/or content of a note. Also updates updated_at.",
)
def update_note(note_id: int, payload: NoteUpdate):
    """Update a note by id, returning the updated record."""
    # Validate that at least one field is provided
    if payload.title is None and payload.content is None:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Build dynamic set clause
    fields = []
    params = []
    if payload.title is not None:
        fields.append("title = %s")
        params.append(payload.title)
    if payload.content is not None:
        fields.append("content = %s")
        params.append(payload.content)

    # Always update updated_at
    fields.append("updated_at = NOW()")

    set_clause = ", ".join(fields)
    params.append(note_id)

    q = f"""
        UPDATE notes
        SET {set_clause}
        WHERE id = %s
        RETURNING id, title, content, created_at, updated_at
    """
    row = execute_returning(q, params)
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    return _row_to_note_out(row)


@router.delete(
    "/{note_id}",
    status_code=204,
    summary="Delete note",
    description="Delete a note by ID. Returns 204 on success and 404 if not found.",
)
def delete_note(note_id: int):
    """Delete a note by id."""
    q = "DELETE FROM notes WHERE id = %s"
    count = execute(q, [note_id])
    if count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
