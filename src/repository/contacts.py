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
        """
        Retrieve a contact from the database based on the provided ID and user.

        :param id: The ID of the contact to retrieve.
        :type id: int
        :param user: The user object representing the owner of the contact.
        :type user: UserOut

        :return: A ContactOut object representing the retrieved contact, if found.
                None if no contact is found with the given ID and user.
        :rtype: ContactOut or None
        """
        contact = (
            self._session.query(Contact)
            .filter(Contact.user_id == user.id, Contact.id == id)
            .first()
        )
        if not contact:
            return None
        return ContactOut(**contact.to_dict())

    async def get_contacts(self, query, user: UserOut) -> list[ContactIn]:
        """
        Retrieve contacts from the database based on the provided query parameters and user.

        :param query: A dictionary containing query parameters to filter contacts.
                        Keys represent fields to filter on, and values represent desired values.
        :type query: dict
        :param user: The user object representing the owner of the contacts.
        :type user: UserOut

        :return: A list of ContactOut objects representing the retrieved contacts.
        :rtype: list[ContactOut]
        """
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
        """
        Create a new contact in the database for the given user.

        :param new_contact: The ContactIn object representing the new contact to be created.
        :type new_contact: ContactIn
        :param user: The user object representing the owner of the contact.
        :type user: UserOut

        :return: A ContactOut object representing the created contact.
        :rtype: ContactOut
        """
        contact = Contact(**new_contact.model_dump(), user_id=user.id)
        self._session.add(contact)
        self._session.commit()
        self._session.refresh(contact)
        return ContactOut(**contact.to_dict())

    async def delete_contact(self, id: int, user: UserOut) -> ContactOut:
        """
        Delete a contact from the database based on the provided ID and user.

        :param id: The ID of the contact to delete.
        :type id: int
        :param user: The user object representing the owner of the contact.
        :type user: UserOut

        :return: A ContactOut object representing the deleted contact, if found and deleted.
                None if no contact is found with the given ID and user.
        :rtype: ContactOut or None
        """
        contact = (
            self._session.query(Contact)
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
        """
        Update an existing contact in the database with new content provided.

        :param id: The ID of the contact to update.
        :type id: int
        :param new_content: The ContactIn object representing the new content
                                    to update the contact with.
        :type new_content: ContactIn
        :param user: The user object representing the owner of the contact.
        :type user: UserOut

        :return: A ContactOut object representing the updated contact.
                None if no contact is found with the given ID and user.
        :rtype: ContactOut or None
        """
        contact = (
            self._session.query(Contact)
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
        """
        Retrieve contacts with upcoming birthdays for the given user within the next 7 days.

        :param user: The user object representing the owner of the contacts.
        :type user: UserOut

        :return: A list of ContactOut objects representing the contacts with upcoming birthdays.
                None if no contacts have upcoming birthdays within the next 7 days.
        :rtype: list[ContactOut] or None
        """
        today = date.today()
        end_date = today + timedelta(days=7)
        contacts_with_birthdays = []
        contacts = self._session.query(Contact).filter(Contact.user_id == user.id).all()
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
