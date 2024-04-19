import unittest
from unittest.mock import MagicMock, AsyncMock

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
        contact = Contact(
            id=1,
            first_name="ksjfsfa",
            last_name="sdfsd",
            email="blabla@blabal.com",
            phone_number="608608608",
            birth_date="2014-04-07",
            additional_data=None,
        )
        self.session.query().filter().first().return_value = contact
        result = await self.contacts_repository.get_contact(id=1, user=self.user)
        self.assertEqual(result, contact)

    # async def test_get_note_found(self):
    #     note = Note()
    #     self.session.query().filter().first.return_value = note
    #     result = await get_note(note_id=1, user=self.user, db=self.session)
    #     self.assertEqual(result, note)

    # async def test_get_note_not_found(self):
    #     self.session.query().filter().first.return_value = None
    #     result = await get_note(note_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)

    # async def test_create_note(self):
    #     body = NoteModel(title="test", description="test note", tags=[1, 2])
    #     tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
    #     self.session.query().filter().all.return_value = tags
    #     result = await create_note(body=body, user=self.user, db=self.session)
    #     self.assertEqual(result.title, body.title)
    #     self.assertEqual(result.description, body.description)
    #     self.assertEqual(result.tags, tags)
    #     self.assertTrue(hasattr(result, "id"))

    # async def test_remove_note_found(self):
    #     note = Note()
    #     self.session.query().filter().first.return_value = note
    #     result = await remove_note(note_id=1, user=self.user, db=self.session)
    #     self.assertEqual(result, note)

    # async def test_remove_note_not_found(self):
    #     self.session.query().filter().first.return_value = None
    #     result = await remove_note(note_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)

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
