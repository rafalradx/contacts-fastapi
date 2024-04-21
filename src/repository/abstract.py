from abc import ABC, abstractmethod
from src.schemas.contacts import ContactIn, ContactOut
from src.schemas.users import UserIn, UserOut


class AbstractContactRepository(ABC):
    """
    An abstract base class defining the interface for a contact repository.

    Concrete implementations of this class must provide implementations for
    the abstract methods defined here.

    """

    @abstractmethod
    def get_contact(self, id: int, current_user: UserOut) -> ContactOut:
        """
        Retrieve a contact from the repository based on the provided ID and user.

        :param id: The ID of the contact to retrieve.
        :type id: int
        :param current_user: The user object representing the current user.
        :type current_user: UserOut

        :return: A ContactOut object representing the retrieved contact.
        :rtype: ContactOut
        """
        ...

    @abstractmethod
    def get_contacts(self, current_user: UserOut) -> list[ContactOut]:
        """
        Retrieve contacts belonging to the current user from the repository.

        :param current_user: The user object representing the current user.
        :type current_user: UserOut

        :return: A list of ContactOut objects representing the retrieved contacts.
        :rtype: List[ContactOut]
        """
        ...

    @abstractmethod
    def create_contact(
        self, new_contact: ContactIn, current_user: UserOut
    ) -> ContactOut:
        """
        Create a new contact in the repository for the current user.

        :param new_contact: The ContactIn object representing the new contact to be created.
        :type new_contact: ContactIn
        :param current_user: The user object representing the current user.
        :type current_user: UserOut

        :return: A ContactOut object representing the created contact.
        :rtype: ContactOut
        """
        ...

    @abstractmethod
    def delete_contact(self, id: int, current_user: UserOut) -> ContactOut:
        """
        Delete a contact from the repository based on the provided ID and user.

        :param id: The ID of the contact to delete.
        :type id: int
        :param current_user: The user object representing the current user.
        :type current_user: UserOut

        :return: A ContactOut object representing the deleted contact.
        :rtype: ContactOut
        """
        ...

    @abstractmethod
    def update_contact(
        self, id: int, contact: ContactIn, current_user: UserOut
    ) -> ContactOut:
        """
        Update an existing contact in the repository with new content provided.

        :param id: The ID of the contact to update.
        :type id: int
        :param contact: The ContactIn object representing the new content
                                   to update the contact with.
        :type contact: ContactIn
        :param current_user: The user object representing the current user.
        :type current_user: UserOut

        :return: A ContactOut object representing the updated contact.
        :rtype: ContactOut
        """
        ...


class AbstractUserRepository(ABC):
    """
    An abstract base class defining the interface for a user repository.

    Concrete implementations of this class must provide implementations for
    the abstract methods defined here.

    """

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserOut:
        """
        Retrieve a user from the repository based on the provided email.

        :param email: The email of the user to retrieve.
        :type email: str

        :return: A UserOut object representing the retrieved user.
        :rtype: UserOut
        """
        ...

    @abstractmethod
    def create_user(self, new_user: UserIn) -> UserOut:
        """
        Create a new user in the repository.

        :param new_user: The UserIn object representing the new user to be created.
        :type new_user: UserIn

        :return: A UserOut object representing the created user.
        :rtype: UserOut
        """
        ...

    @abstractmethod
    def update_token(self, user: UserOut, token: str | None) -> None:
        """
        Update the authentication token for a user in the repository.

        :param user: The user object representing the user to update.
        :type user: UserOut
        :param token: The new authentication token for the user.
                          None if the token should be removed.
        :param toke: str

        :return: None
        """
        ...

    @abstractmethod
    def confirm_email(self, email: str) -> None:
        """
        Confirm the email address of a user in the repository.

        :param email: The email address to confirm.
        :type email: str

        :return: None
        """
        ...

    @abstractmethod
    def update_avatar(self, email, url: str) -> UserOut:
        """
        Update the avatar URL for a user in the repository.

        :param email: The email address of the user to update.
        :type email: str
        :param url: The new avatar URL for the user.
        :type url: str

        :return: A UserOut object representing the updated user.
        :rtype: UserOut
        """
        ...
