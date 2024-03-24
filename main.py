from fastapi import FastAPI, Path, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles

from abstract_repository import AbstractContactRepository
from dependencies import get_repository
from models import ContactOut, ContactIn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/contacts/{contact_id}")
async def read_contact(
    contact_id: int = Path(description="The ID of note to be acquired."),
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    contact = contact_repository.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@app.get("/contacts")
async def read_contacts(
    note_repository: AbstractContactRepository = Depends(get_repository),
) -> list[ContactOut]:
    notes = note_repository.get_contacts()
    return notes


@app.post("/contacts", status_code=status.HTTP_201_CREATED)
async def create_contact(
    note: ContactIn,
    note_repository: AbstractContactRepository = Depends(get_repository),
):
    new_note = note_repository.create_contact(note)
    return new_note
