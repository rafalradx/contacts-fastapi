from src.repository.abstract import AbstractUserRepository
from src.database.models import User
from src.schemas.users import UserIn, UserOut
from sqlalchemy.orm import Session
from libgravatar import Gravatar


class UserRepository(AbstractUserRepository):
    def __init__(self, db_session: Session):
        """
        Initializes the UserRepository with the provided SQLAlchemy database session.

        :param db_session: The SQLAlchemy database session.
        :type db_session: Session
        """
        self._session = db_session

    async def get_user_by_email(self, email: str) -> UserOut:
        """
        Retrieve a user from the repository based on the provided email.

        :param email: The email of the user to retrieve.
        :type email: str

        :return: A UserOut object representing the retrieved user.
        :rtype: UserOut
        """
        return self._session.query(User).filter(User.email == email).first()

    async def create_user(self, new_user: UserIn) -> UserOut:
        """
        Create a new user in the repository with an avatar from Gravatar.

        :param new_user: The UserIn object representing the new user to be created.
        :type new_user: UserIn

        :return: A UserOut object representing the created user.
        :rtype: UserOut
        """
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
        """
        Update the refresh token for a user in the repository for authentication.

        :param user: The user object representing the user to update.
        :type user: User
        :param token: The new authentication token for the user.
                          None if the token should be removed.
        :type token: str

        :return: None
        """
        user.refresh_token = token
        self._session.commit()

    async def confirm_email(self, email: str) -> None:
        """
        Confirm the email address of a user in the repository.

        :param email: The email address to confirm.
        :type email: str

        :return: None
        """
        user = await self.get_user_by_email(email)
        user.confirmed = True
        self._session.commit()

    async def update_avatar(self, email, url: str) -> UserOut:
        """
        Update the avatar URL for a user in the repository.

        :param email: The email address of the user to update.
        :type email: str
        :param url: The new avatar URL for the user.
        :type url: str

        :return: A UserOut object representing the updated user.
        :rtype: UserOut
        """
        user = await self.get_user_by_email(email)
        user.avatar = url
        self._session.commit()
        return user
