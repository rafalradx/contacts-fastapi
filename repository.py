from abstract_repository import AbstractNoteRepository
from db import Note
from models import NoteIn, NoteOut


class NoteRepository(AbstractNoteRepository):
    def __init__(self, session):
        self._session = session

    def get_note(self, id) -> NoteOut:
        note = self._session.get(Note, id)
        return NoteOut(name=note.name, description=note.description, done=note.done, id=note.id)

    def get_notes(self) -> list[NoteOut]:
        return [NoteOut(name=note.name, description=note.description, done=note.done, id=note.id) for note in self._session.query(Note).all()]

    def create_note(self, note: NoteIn) -> NoteOut:
        note = Note(name=note.name, description=note.description, done=note.done)
        self._session.add(note)
        self._session.commit()
        self._session.refresh(note)
        return NoteOut(name=note.name, description=note.description, done=note.done, id=note.id)

    def delete_note(self, note_id: int):
        ...


class MongoNoteRepository(AbstractNoteRepository):
    def __init__(self, session):
        self._session = session

    def get_note(self, id) -> NoteOut:
        # Tutaj logika pozyskująca dane z mongoengine
        # return NoteOut(name=note.name, description=note.description, done=note.done, id=note.id)
        ...

    def get_notes(self) -> list[NoteOut]:
        # Tutaj logika pozyskująca dane z mongoengine
        # return [NoteOut(name=note.name, description=note.description, done=note.done, id=note.id) for note in self._session.query(Note).all()]
        ...

    def create_note(self, note: NoteIn) -> NoteOut:
        # Tutaj logika pozyskująca dane z mongoengine
        # return NoteOut(name=note.name, description=note.description, done=note.done, id=note.id)
        ...