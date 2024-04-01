from fastapi import APIRouter, Path, Depends, HTTPException, status, Query
from src.repository.abstract import AbstractContactRepository
from dependencies import get_repository
from src.schemas.contacts import ContactOut, ContactIn

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/{contact_id}", status_code=status.HTTP_200_OK)
async def read_contact(
    contact_id: int = Path(description="The ID of contact to be acquired."),
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    contact = contact_repository.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@router.get("", status_code=status.HTTP_200_OK)
async def read_contacts(
    first_name: str | None = Query(default=None, max_length=50),
    last_name: str | None = Query(default=None, max_length=50),
    email: str | None = Query(default=None, max_length=50),
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> list[ContactOut]:
    query = {"first_name": first_name, "last_name": last_name, "email": email}
    contacts = contact_repository.get_contacts(query)
    return contacts


@router.get("/birthdays", status_code=status.HTTP_200_OK)
async def read_upcoming_birthdays(
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> list[ContactOut]:
    contacts = contact_repository.get_upcoming_birthdays()
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contacts


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactIn,
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    new_contact = contact_repository.create_contact(contact)
    return new_contact


@router.delete("/{contact_id}", status_code=status.HTTP_200_OK)
async def remove_contact(
    contact_id: int = Path(description="The ID of contact to be removed."),
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    contact = contact_repository.delete_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@router.put("/{contact_id}", status_code=status.HTTP_200_OK)
async def update_contact(
    contact: ContactIn,
    contact_id: int = Path(description="The ID of contact to be updated."),
    contact_repository: AbstractContactRepository = Depends(get_repository),
) -> ContactOut:
    updated_contact = contact_repository.update_contact(contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated_contact
