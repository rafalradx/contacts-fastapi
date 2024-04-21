import unittest
from unittest.mock import MagicMock, AsyncMock, Mock

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas.contacts import ContactIn, ContactOut
from src.schemas.users import UserOut
from src.repository.contacts import ContactRepository
from datetime import date, timedelta


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=Session)
        self.user = UserOut(
            id=1,
            username="karaczan",
            email="wombat@wombat.com",
            created_at="2024-04-07 13:12:00.940",
            avatar="sdfs",
        )
        self.contacts_repository = ContactRepository(db_session=self.session)
        self.contact = Contact(
            id=1,
            first_name="ksjfsfa",
            last_name="sdfsd",
            email="blabla@blabal.com",
            phone_number="608608608",
            birth_date="2014-04-07",
            additional_data=None,
        )
        self.contact_out = ContactOut(**self.contact.to_dict())
        self.contact_in = ContactIn(
            first_name="Jack",
            last_name="Black",
            email="Jack@black.com",
            phone_number="776667123",
            birth_date="1978-02-12",
            additional_data=None,
        )

    async def test_get_contact(self):

        contact_mock = MagicMock(spec=Contact)
        contact_mock.to_dict.return_value = self.contact.to_dict()
        query_mock = self.session.query.return_value
        query_mock.filter.return_value.first.return_value = contact_mock
        result = await self.contacts_repository.get_contact(id=1, user=self.user)
        self.assertEqual(result, self.contact_out)

    async def test_get_note_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await self.contacts_repository.get_contact(id=1, user=self.user)
        self.assertIsNone(result)

    async def test_create_contact(self):
        contact_dict = self.contact_in.model_dump()
        contact_dict["id"] = 666
        contact_mock = MagicMock(ContactOut)
        contact_mock.model_dump.return_value = contact_dict

        result = await self.contacts_repository.create_contact(
            new_contact=contact_mock, user=self.user
        )
        self.assertEqual(result.first_name, self.contact_in.first_name)
        self.assertEqual(result.last_name, self.contact_in.last_name)
        self.assertEqual(result.email, self.contact_in.email)
        self.assertEqual(result.phone_number, self.contact_in.phone_number)
        self.assertEqual(result.birth_date, self.contact_in.birth_date)
        self.assertEqual(result.additional_data, self.contact_in.additional_data)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(result.id, self.user.id)

    async def test_delete_contact_found(self):

        contact_mock = MagicMock(spec=Contact)
        contact_mock.to_dict.return_value = self.contact.to_dict()
        query_mock = self.session.query.return_value
        query_mock.filter.return_value.first.return_value = contact_mock
        result = await self.contacts_repository.delete_contact(id=1, user=self.user)
        self.assertEqual(result, self.contact_out)

    async def test_delete_note_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await self.contacts_repository.delete_contact(id=1, user=self.user)
        self.assertIsNone(result)

    async def test_update_contact_found(self):

        contact_mock = AsyncMock(spec=Contact)
        contact_mock.to_dict.return_value = self.contact.to_dict()
        query_mock = self.session.query.return_value
        query_mock.filter.return_value.first.return_value = contact_mock
        result = await self.contacts_repository.update_contact(
            id=1, new_content=contact_mock, user=self.user
        )
        self.assertEqual(result, self.contact_out)

    async def test_update_contact_not_found(self):

        contact_mock = AsyncMock(spec=Contact)
        contact_mock.to_dict.return_value = self.contact.to_dict()
        query_mock = self.session.query.return_value
        query_mock.filter.return_value.first.return_value = None
        result = await self.contacts_repository.update_contact(
            id=1, new_content=contact_mock, user=self.user
        )
        self.assertIsNone(result, self.contact_out)

    async def test_get_upcoming_birthdays_found(self):
        contact_with_birthday = self.contact
        today = date.today()
        birthdate = date(year=today.year - 10, month=today.month, day=today.day)
        contact_with_birthday.birth_date = birthdate + timedelta(days=2)
        contact_mock = AsyncMock(spec=Contact)
        contact_mock.to_dict.return_value = contact_with_birthday.to_dict()
        contact_mock.birth_date.return_values = contact_with_birthday.birth_date
        contact_list = [
            contact_mock,
            contact_mock,
            contact_mock,
        ]
        query_mock = self.session.query.return_value
        query_mock.query.return_value.filter.return_value.all = contact_list
        result = await self.contacts_repository.get_upcoming_birthdays(user=self.user)
        self.assertEqual(result, contact_list)

    async def test_get_upcoming_birthdays_not_found(self):
        contact_no_birthday = self.contact
        contact_no_birthday.birth_date = date.today() - timedelta(days=2)
        contact_list = [contact_no_birthday, contact_no_birthday, contact_no_birthday]
        query_mock = self.session.query.return_value
        query_mock.query.return_value.filter.return_value.all.return_value = (
            contact_list
        )
        result = await self.contacts_repository.get_upcoming_birthdays(user=self.user)
        self.assertIsNone(result, contact_list)


if __name__ == "__main__":
    unittest.main()
