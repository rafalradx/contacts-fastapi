from fastapi import FastAPI, Path, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles

from abstract_repository import AbstractContactRepository
from dependencies import get_repository
from models import ContactOut, ContactIn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/notes/{note_id}")
async def read_note(
    note_id: int = Path(description="The ID of note to be acquired."),
    note_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    note = note_repository.get_note(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return note


@app.get("/notes")
async def read_notes(
    note_repository: AbstractContactRepository = Depends(get_repository),
) -> list[ContactOut]:
    notes = note_repository.get_notes()
    return notes


@app.post("/notes", status_code=status.HTTP_201_CREATED)
async def create_note(
    note: ContactIn,
    note_repository: AbstractContactRepository = Depends(get_repository),
):
    new_note = note_repository.create_note(note)
    return new_note
