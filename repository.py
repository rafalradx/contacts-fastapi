from abstract_repository import AbstractContactRepository
from db import Contact
from models import ContactIn, ContactOut


class ContactRepository(AbstractContactRepository):
    def __init__(self, session):
        self._session = session

    def get_note(self, id) -> ContactOut:
        note = self._session.get(Contact, id)
        return ContactOut(
            name=note.name, description=note.description, done=note.done, id=note.id
        )

    def get_notes(self) -> list[ContactIn]:
        return [
            ContactOut(
                name=note.name, description=note.description, done=note.done, id=note.id
            )
            for note in self._session.query(Contact).all()
        ]

    def create_note(self, note: ContactIn) -> ContactOut:
        note = Contact(name=note.name, description=note.description, done=note.done)
        self._session.add(note)
        self._session.commit()
        self._session.refresh(note)
        return ContactOut(
            name=note.name, description=note.description, done=note.done, id=note.id
        )

    def delete_note(self, id: int):
        contact = self._session.get(Contact, id)
        self._session.delete(contact)
        return ContactOut()


# class MongoContactRepository(AbstractContactRepository):
#     def __init__(self, session):
#         self._session = session

#     def get_note(self, id) -> NoteOut:
#         # Tutaj logika pozyskująca dane z mongoengine
#         # return NoteOut(name=note.name, description=note.description, done=note.done, id=note.id)
#         ...

#     def get_notes(self) -> list[NoteOut]:
#         # Tutaj logika pozyskująca dane z mongoengine
#         # return [NoteOut(name=note.name, description=note.description, done=note.done, id=note.id) for note in self._session.query(Note).all()]
#         ...

#     def create_note(self, note: NoteIn) -> NoteOut:
#         # Tutaj logika pozyskująca dane z mongoengine
#         # return NoteOut(name=note.name, description=note.description, done=note.done, id=note.id)
#         ...
