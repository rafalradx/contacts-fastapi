from src.repository.abstract import AbstractContactRepository
from src.database.models import Contact
from src.schemas.contacts import ContactIn, ContactOut
from src.schemas.users import UserOut
from datetime import date, timedelta
from sqlalchemy.orm import Session


class ContactRepository(AbstractContactRepository):
    def __init__(self, db_session: Session):
        self._session = db_session

    async def get_contact(self, id: int, user: UserOut) -> ContactOut:
        contact = (
            self._session.query(Contact)
            .filter(Contact.user_id == user.id, Contact.id == id)
            .first()
        )
        if not contact:
            return None
        return ContactOut(**contact.to_dict())

    async def get_contacts(self, query, user: UserOut) -> list[ContactIn]:
        query = {field: value for field, value in query.items() if value is not None}

        if query:
            return [
                ContactOut(**contact.to_dict())
                for contact in self._session.query(Contact)
                .filter(Contact.user_id == user.id)
                .filter_by(**query)
                .all()
            ]

        return [
            ContactOut(**contact.to_dict())
            for contact in self._session.query(Contact)
            .filter(Contact.user_id == user.id)
            .all()
        ]

    async def create_contact(self, new_contact: ContactIn, user: UserOut) -> ContactOut:
        contact = Contact(**new_contact.model_dump(), user_id=user.id)
        self._session.add(contact)
        self._session.commit()
        self._session.refresh(contact)
        return ContactOut(**contact.to_dict())

    async def delete_contact(self, id: int, user: UserOut) -> ContactOut:
        contact = (
            await self._session.query(Contact)
            .filter(Contact.user_id == user.id, Contact.id == id)
            .first()
        )
        if not contact:
            return None
        self._session.delete(contact)
        self._session.commit()
        return ContactOut(**contact.to_dict())

    async def update_contact(
        self, id: int, new_content: ContactIn, user: UserOut
    ) -> ContactOut:
        contact = (
            await self._session.query(Contact)
            .filter(Contact.user_id == user.id, Contact.id == id)
            .first()
        )
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

    async def get_upcoming_birthdays(self, user: UserOut) -> list[ContactIn]:
        today = date.today()
        end_date = today + timedelta(days=7)
        contacts_with_birthdays = []
        contacts = (
            await self._session.query(Contact).filter(Contact.user_id == user.id).all()
        )
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
