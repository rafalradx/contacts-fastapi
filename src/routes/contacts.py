import pickle
from fastapi import APIRouter, Path, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from src.repository.abstract import AbstractContactRepository, AbstractUserRepository
from dependencies import get_contacts_repository, get_users_repository, get_redis_client
from src.schemas.contacts import ContactOut, ContactIn
from src.schemas.users import UserOut
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/contacts", tags=["contacts"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
request_limiter = RateLimiter(times=2, seconds=5)


async def get_current_user(
    token: OAuth2PasswordBearer = Depends(oauth2_scheme),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
    redis: Redis = Depends(get_redis_client),
) -> UserOut:
    """
    Get the current authenticated user.

    :param token: The OAuth2 token.
    :type token: str

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param redis: The Redis client.
    :type redis: Redis

    :param auth_service: The JWT handling service.
    :type auth_service: HandleJWT

    :return: The current authenticated user.
    :rtype: UserOut

    :raises HTTPException 401: If the credentials are invalid.
    """
    user_email = await auth_service.get_email_from_access_token(token=token)
    user = await redis.get(f"user:{user_email}")
    if user is not None:
        return pickle.loads(user)

    user = await users_repository.get_user_by_email(user_email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    await redis.set(f"user:{user_email}", pickle.dumps(user))
    await redis.expire(f"user:{user_email}", 900)
    return user


@router.get(
    "/{contact_id}",
    dependencies=[Depends(request_limiter)],
    status_code=status.HTTP_200_OK,
)
async def read_contact(
    contact_id: int = Path(description="The ID of contact to be acquired."),
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(get_current_user),
) -> ContactOut:
    """
    Get a contact by ID for authorized user

    :param contact_id: The ID of the contact.
    :type contact_id: int

    :param contacts_repository: The repository for contact data.
    :type contacts_repository: AbstractContactRepository

    :param current_user: The current authenticated user .
    :type current_user: UserOut

    :return: The contact.
    :rtype: ContactOut

    :raises HTTPException 404: If the contact is not found.
    """
    contact = await contacts_repository.get_contact(contact_id, current_user)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@router.get("", dependencies=[Depends(request_limiter)], status_code=status.HTTP_200_OK)
async def read_contacts(
    first_name: str | None = Query(default=None, max_length=50),
    last_name: str | None = Query(default=None, max_length=50),
    email: str | None = Query(default=None, max_length=50),
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(get_current_user),
) -> list[ContactOut]:
    """
    Get contacts based on query parameters for authorized user

    :param first_name: The first name of the contact (optional).
    :type first_name: str, optional

    :param last_name: The last name of the contact (optional).
    :type last_name: str, optional

    :param email: The email address of the contact (optional).
    :type email: str, optional

    :param contacts_repository: The repository for contact data.
    :type contacts_repository: AbstractContactRepository

    :param current_user: The current authenticated user.
    :type current_user: UserOut

    :return: The list of contacts.
    :rtype: List[ContactOut]
    """
    query = {"first_name": first_name, "last_name": last_name, "email": email}
    contacts = await contacts_repository.get_contacts(query, current_user)
    return contacts


@router.get(
    "/birthdays",
    dependencies=[Depends(request_limiter)],
    status_code=status.HTTP_200_OK,
)
async def read_upcoming_birthdays(
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(get_current_user),
) -> list[ContactOut]:
    """
    Get a list of contacts with upcoming birthdays (7 days) for authorized user.

    :param contacts_repository: The repository for contact data.
    :type contacts_repository: AbstractContactRepository

    :param current_user: The current authenticated user.
    :type current_user: UserOut

    :return: The list of contacts with upcoming birthdays.
    :rtype: List[ContactOut]

    :raises HTTPException 404: If no upcoming birthdays are found.
    """
    contacts = await contacts_repository.get_upcoming_birthdays(current_user)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contacts


@router.post(
    "", dependencies=[Depends(request_limiter)], status_code=status.HTTP_201_CREATED
)
async def create_contact(
    contact: ContactIn,
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(get_current_user),
) -> ContactOut:
    """
    Create a new contact for an authorized user

    :param contact: The contact data to create.
    :type contact: ContactIn

    :param contacts_repository: The repository for contact data.
    :type contacts_repository: AbstractContactRepository

    :param current_user: The current authenticated user.
    :type current_user: UserOut

    :return: The newly created contact.
    :rtype: ContactOut
    """
    new_contact = await contacts_repository.create_contact(contact, current_user)
    return new_contact


@router.delete(
    "/{contact_id}",
    dependencies=[Depends(request_limiter)],
    status_code=status.HTTP_200_OK,
)
async def remove_contact(
    contact_id: int = Path(description="The ID of contact to be removed."),
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(get_current_user),
) -> ContactOut:
    """
    Remove a contact from database by ID for authorized user.

    :param contact_id: The ID of the contact to be removed.
    :type contact_id: int

    :param contacts_repository: The repository for contact data.
    :type contacts_repository: AbstractContactRepository

    :param current_user: The current authenticated user.
    :type current_user: UserOut

    :return: The removed contact.
    :rtype: ContactOut

    :raises HTTPException 404: If the contact with the specified ID is not found.
    """
    contact = contacts_repository.delete_contact(contact_id, current_user)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@router.put(
    "/{contact_id}",
    dependencies=[Depends(request_limiter)],
    status_code=status.HTTP_200_OK,
)
async def update_contact(
    contact: ContactIn,
    contact_id: int = Path(description="The ID of contact to be updated."),
    contacts_repository: AbstractContactRepository = Depends(get_contacts_repository),
    current_user: UserOut = Depends(get_current_user),
) -> ContactOut:
    """
    Update a contact by ID for authorized user.

    :param contact: The updated contact data.
    :type contact: ContactIn

    :param contact_id: The ID of the contact to be updated.
    :type contact_id: int

    :param contacts_repository: The repository for contact data.
    :type contacts_repository: AbstractContactRepository

    :param current_user: The current authenticated user.
    :type current_user: UserOut

    :return: The updated contact.
    :rtype: ContactOut

    :raises HTTPException 404: If the contact with the specified ID is not found.
    """
    updated_contact = contacts_repository.update_contact(
        contact_id, contact, current_user
    )
    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated_contact
