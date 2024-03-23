from fastapi import FastAPI, Path, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles

from abstract_repository import AbstractNoteRepository
from dependencies import get_repository
from models import NoteOut, NoteIn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/notes/{note_id}")
async def read_note(
        note_id: int = Path(
            description="The ID of note to be acquired.",
            le=10,
            gt=0
        ),
        note_repository: AbstractNoteRepository = Depends(get_repository)) -> NoteOut:
    note = note_repository.get_note(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return note


@app.get("/notes")
async def read_notes(
        note_repository: AbstractNoteRepository = Depends(get_repository)
) -> list[NoteOut]:
    notes = note_repository.get_notes()
    return notes


@app.post("/notes", status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn, note_repository: AbstractNoteRepository = Depends(get_repository)):
    new_note = note_repository.create_note(note)
    return new_note
