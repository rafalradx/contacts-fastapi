import unittest
from unittest.mock import MagicMock, AsyncMock, Mock

from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas.contacts import ContactIn, ContactOut
from src.schemas.users import UserIn, UserOut
from src.repository.contacts import ContactRepository


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
        contact_in = ContactIn(
            first_name="Jack",
            last_name="Black",
            email="Jack@black.com",
            phone_number="776667123",
            birth_date="1978-02-12",
            additional_data=None,
        )
        contact_dict = contact_in.model_dump()
        contact_dict["id"] = 666
        contact_mock = MagicMock(ContactOut)
        contact_mock.model_dump.return_value = contact_dict

        result = await self.contacts_repository.create_contact(
            new_contact=contact_mock, user=self.user
        )
        self.assertEqual(result.first_name, contact_in.first_name)
        self.assertEqual(result.last_name, contact_in.last_name)
        self.assertEqual(result.email, contact_in.email)
        self.assertEqual(result.phone_number, contact_in.phone_number)
        self.assertEqual(result.birth_date, contact_in.birth_date)
        self.assertEqual(result.additional_data, contact_in.additional_data)
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

    # async def test_update_note_found(self):
    #     body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
    #     tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
    #     note = Note(tags=tags)
    #     self.session.query().filter().first.return_value = note
    #     self.session.query().filter().all.return_value = tags
    #     self.session.commit.return_value = None
    #     result = await update_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertEqual(result, note)

    # async def test_update_note_not_found(self):
    #     body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
    #     self.session.query().filter().first.return_value = None
    #     self.session.commit.return_value = None
    #     result = await update_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertIsNone(result)

    # async def test_update_status_note_found(self):
    #     body = NoteStatusUpdate(done=True)
    #     note = Note()
    #     self.session.query().filter().first.return_value = note
    #     self.session.commit.return_value = None
    #     result = await update_status_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertEqual(result, note)

    # async def test_update_status_note_not_found(self):
    #     body = NoteStatusUpdate(done=True)
    #     self.session.query().filter().first.return_value = None
    #     self.session.commit.return_value = None
    #     result = await update_status_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
