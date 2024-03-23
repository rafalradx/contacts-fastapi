from abstract_repository import AbstractNoteRepository
from db import SessionLocal
from repository import NoteRepository


def get_repository() -> AbstractNoteRepository:
    return NoteRepository(SessionLocal())
