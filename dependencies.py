from abstract_repository import AbstractContactRepository
from db import SessionLocal
from repository import ContactRepository


def get_repository() -> AbstractContactRepository:
    return ContactRepository(SessionLocal())
