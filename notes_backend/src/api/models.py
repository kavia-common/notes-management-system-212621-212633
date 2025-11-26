from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class NoteCreate(BaseModel):
    """Payload for creating a note."""
    title: str = Field(..., description="Title of the note", min_length=1)
    content: str = Field(..., description="Content/body of the note")


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Payload for updating a note."""
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1)
    content: Optional[str] = Field(None, description="Updated content/body of the note")


# PUBLIC_INTERFACE
class NoteOut(BaseModel):
    """Note representation returned by the API."""
    id: int = Field(..., description="Unique identifier of the note")
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content/body of the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
