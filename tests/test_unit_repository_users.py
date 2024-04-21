import unittest
from unittest.mock import MagicMock, AsyncMock, Mock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.users import UserIn, UserOut
from src.repository.users import UserRepository


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=Session)
        self.users_repository = UserRepository(db_session=self.session)
        self.user_out = UserOut(
            id=1,
            username="karaczan",
            email="wombat@wombat.com",
            created_at="2024-04-07 13:12:00.940",
            avatar="sdfs",
        )
        self.user_in = UserIn(
            username="Karaczan", email="karaczan@ant.com", password="abcd1234"
        )

    async def test_get_user_by_email_found(self):
        email = "jach@black.com"
        self.session.query().filter().first.return_value = self.user_out
        result = await self.users_repository.get_user_by_email(email)
        self.assertEqual(result, self.user_out)

    async def test_update_token(self):
        user = MagicMock(spec=User)
        result = await self.users_repository.update_token(
            user=user, token="this is token"
        )
        self.assertIsNone(result)

    async def test_update_token_none_token(self):
        user = MagicMock(spec=User)
        result = await self.users_repository.update_token(user=user, token=None)
        self.assertIsNone(result)

    async def test_confirm_email(self):
        result = await self.users_repository.confirm_email(email="not@work.com")
        self.assertIsNone(result)

    async def test_update_avatar(self):
        self.session.query().filter().first.return_value = self.user_out
        avatar = "www.avatar.com.pl"
        result = await self.users_repository.update_avatar(
            email="not@work.com", url=avatar
        )
        self.assertEqual(result.avatar, avatar)


if __name__ == "__main__":
    unittest.main()
