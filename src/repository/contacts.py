from src.repository.abstract import AbstractContactRepository
from src.database.models import Contact
from src.schemas.contacts import ContactIn, ContactOut
from datetime import date, timedelta


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

    def get_upcoming_birthdays(self) -> list[ContactIn]:
        today = date.today()
        end_date = today + timedelta(days=7)
        contacts_with_birthdays = []
        contacts = self._session.query(Contact).all()
        if today.year == end_date.year:
            for contact in contacts:
                dt = (
                    date(
                        year=today.year,
                        month=contact.birth_date.month,
                        day=contact.birth_date.day,
                    )
                    - today
                )
                if dt.days <= 7 and dt.days >= 0:
                    contacts_with_birthdays.append(contact)
        else:
            for contact in contacts:
                dt = (
                    date(
                        year=today.year,
                        month=contact.birth_date.month,
                        day=contact.birth_date.day,
                    )
                    - today
                )
                if dt.days <= 7 and dt.days >= 0:
                    contacts_with_birthdays.append(contact)
                elif dt.days < 0:
                    dt = (
                        date(
                            year=today.year + 1,
                            month=contact.birth_date.month,
                            day=contact.birth_date.day,
                        )
                        - today
                    )
                    if dt.days <= 7:
                        contacts_with_birthdays.append(contact)

        if not contacts_with_birthdays:
            return None
        return [ContactOut(**contact.to_dict()) for contact in contacts_with_birthdays]
