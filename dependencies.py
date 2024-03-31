from src.repository.abstract import AbstractContactRepository
from src.database.db import SessionLocal
from src.repository.contacts import ContactRepository


def get_repository() -> AbstractContactRepository:
    return ContactRepository(SessionLocal())
