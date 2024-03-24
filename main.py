from fastapi import FastAPI, Path, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles

from abstract_repository import AbstractContactRepository
from dependencies import get_repository
from models import ContactOut, ContactIn

app = FastAPI()


@app.get("/contacts/{contact_id}")
async def read_contact(
    contact_id: int = Path(description="The ID of contact to be acquired."),
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    contact = contact_repository.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@app.get("/contacts")
async def read_contacts(
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> list[ContactOut]:
    contacts = contact_repository.get_contacts()
    return contacts


@app.post("/contacts", status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactIn,
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    new_contact = contact_repository.create_contact(contact)
    return new_contact


@app.delete("/contacts{contact_id}", status_code=status.HTTP_200_OK)
async def remove_contact(
    contact_id: int = Path(description="The ID of contact to be removed."),
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    contact = contact_repository.delete_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@app.put("/contacts{contact_id}", status_code=status.HTTP_200_OK)
async def update_contact(
    contact: ContactIn,
    contact_id: int = Path(description="The ID of contact to be updated."),
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    updated_contact = contact_repository.update_contact(contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated_contact
