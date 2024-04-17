from src.repository.abstract import AbstractUserRepository
from src.database.models import User
from src.schemas.users import UserIn, UserOut
from sqlalchemy.orm import Session
from libgravatar import Gravatar


class UserRepository(AbstractUserRepository):
    def __init__(self, db_session: Session):
        self._session = db_session

    async def get_user_by_email(self, email: str) -> UserOut:
        return self._session.query(User).filter(User.email == email).first()

    async def create_user(self, new_user: UserIn) -> UserOut:
        avatar = None
        try:
            gravatar = Gravatar(new_user.email)
            avatar = gravatar.get_image()
        except Exception as e:
            print(e)
        new_user = User(**new_user.model_dump(), avatar=avatar)
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)
        return UserOut(**new_user.to_dict())

    async def update_token(self, user: User, token: str | None) -> None:
        user.refresh_token = token
        self._session.commit()

    async def confirm_email(self, email: str) -> None:
        user = await self.get_user_by_email(email)
        user.confirmed = True
        self._session.commit()

    async def update_avatar(self, email, url: str) -> UserOut:
        user = await self.get_user_by_email(email)
        user.avatar = url
        self._session.commit()
        return user
