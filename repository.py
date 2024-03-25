from abstract_repository import AbstractContactRepository
from db import Contact
from models import ContactIn, ContactOut


class ContactRepository(AbstractContactRepository):
    def __init__(self, session):
        self._session = session

    def get_contact(self, id) -> ContactOut:
        contact = self._session.get(Contact, id)
        if not contact:
            return None
        return ContactOut(**contact.to_dict())

    def get_contacts(self, query) -> list[ContactIn]:
        query = {field: value for field, value in query.items() if value is not None}

        if query:
            return [
                ContactOut(**contact.to_dict())
                for contact in self._session.query(Contact).filter_by(**query)
            ]

        return [
            ContactOut(**contact.to_dict())
            for contact in self._session.query(Contact).all()
        ]

    def create_contact(self, contact: ContactIn) -> ContactOut:
        contact = Contact(**contact.model_dump())
        self._session.add(contact)
        self._session.commit()
        self._session.refresh(contact)
        return ContactOut(**contact.to_dict())

    def delete_contact(self, id: int) -> ContactOut:
        contact = self._session.get(Contact, id)
        if not contact:
            return None
        self._session.delete(contact)
        self._session.commit()
        return ContactOut(**contact.to_dict())

    def update_contact(self, id: int, new_content: ContactIn) -> ContactOut:
        contact = self._session.get(Contact, id)
        if not contact:
            return None
        contact.first_name = new_content.first_name
        contact.last_name = new_content.last_name
        contact.email = new_content.email
        contact.birth_date = new_content.birth_date
        contact.phone_number = new_content.phone_number
        contact.additional_data = new_content.additional_data
        self._session.add(contact)
        self._session.commit()
        return ContactOut(**contact.to_dict())
