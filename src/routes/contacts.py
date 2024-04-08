from fastapi import APIRouter, Path, Depends, HTTPException, status, Query
from src.repository.abstract import AbstractContactRepository
from dependencies import get_contacts_repository
from src.schemas.contacts import ContactOut, ContactIn
from src.schemas.users import UserOut
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/{contact_id}", status_code=status.HTTP_200_OK)
async def read_contact(
    id: int = Path(description="The ID of contact to be acquired."),
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(auth_service.get_current_user),
) -> ContactOut:
    contact = await contacts_repository.get_contact(id, current_user)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@router.get("", status_code=status.HTTP_200_OK)
async def read_contacts(
    first_name: str | None = Query(default=None, max_length=50),
    last_name: str | None = Query(default=None, max_length=50),
    email: str | None = Query(default=None, max_length=50),
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(auth_service.get_current_user),
) -> list[ContactOut]:
    query = {"first_name": first_name, "last_name": last_name, "email": email}
    contacts = await contacts_repository.get_contacts(query, current_user)
    return contacts


@router.get("/birthdays", status_code=status.HTTP_200_OK)
async def read_upcoming_birthdays(
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(auth_service.get_current_user),
) -> list[ContactOut]:
    contacts = await contacts_repository.get_upcoming_birthdays(current_user)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contacts


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactIn,
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(auth_service.get_current_user),
) -> ContactOut:
    new_contact = await contacts_repository.create_contact(contact, current_user)
    return new_contact


@router.delete("/{contact_id}", status_code=status.HTTP_200_OK)
async def remove_contact(
    contact_id: int = Path(description="The ID of contact to be removed."),
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(auth_service.get_current_user),
) -> ContactOut:
    contact = contacts_repository.delete_contact(contact_id, current_user)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@router.put("/{contact_id}", status_code=status.HTTP_200_OK)
async def update_contact(
    contact: ContactIn,
    contact_id: int = Path(description="The ID of contact to be updated."),
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(auth_service.get_current_user),
) -> ContactOut:
    updated_contact = contacts_repository.update_contact(
        contact_id, contact, current_user
    )
    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated_contact
