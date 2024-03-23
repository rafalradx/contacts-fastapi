from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    name: str
    description: str
    done: bool


class NoteOut(NoteIn):
    id: int = Field(default=1, ge=1)
