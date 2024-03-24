from abstract_repository import AbstractContactRepository
from db import Contact
from models import ContactIn, ContactOut


class ContactRepository(AbstractContactRepository):
    def __init__(self, session):
        self._session = session

    def get_contact(self, id) -> ContactOut:
        contact = self._session.get(Contact, id)
        return ContactOut(**contact.to_dict())

    def get_contacts(self) -> list[ContactIn]:
        return [
            ContactOut(**contact.to_dict())
            for contact in self._session.query(Contact).all()
        ]

    def create_contact(self, contact: ContactIn) -> ContactOut:
        contact = Contact(**contact.model_dump())
        self._session.add(contact)
        self._session.commit()
        self._session.refresh(contact)  # contact gets id
        return ContactOut(**contact.to_dict())

    def delete_contact(self, id: int):
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
