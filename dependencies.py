from src.repository.abstract import AbstractContactRepository, AbstractUserRepository
from src.database.db import SessionLocal
from src.repository.contacts import ContactRepository
from src.repository.users import UserRepository


def get_contacts_repository() -> AbstractContactRepository:
    return ContactRepository(SessionLocal())


def get_users_repository() -> AbstractUserRepository:
    return UserRepository(SessionLocal())
