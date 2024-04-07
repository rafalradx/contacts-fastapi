from abc import ABC, abstractmethod
from src.schemas.contacts import ContactIn, ContactOut
from src.schemas.users import UserIn, UserOut, UserCreated


class AbstractContactRepository(ABC):

    @abstractmethod
    def get_contact(self, id: int, current_user: UserOut) -> ContactOut: ...

    @abstractmethod
    def get_contacts(self, current_user: UserOut) -> list[ContactOut]: ...

    @abstractmethod
    def create_contact(
        self, new_contact: ContactIn, current_user: UserOut
    ) -> ContactOut: ...

    @abstractmethod
    def delete_contact(self, id: int, current_user: UserOut) -> ContactOut: ...

    @abstractmethod
    def update_contact(
        self, id: int, contact: ContactIn, current_user: UserOut
    ) -> ContactOut: ...


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> UserOut: ...

    @abstractmethod
    def create_user(self, new_user: UserIn) -> UserCreated: ...

    @abstractmethod
    def update_token(self, user: UserOut, token: str | None) -> None: ...

    @abstractmethod
    def confirm_email(self, email: str) -> None: ...

    @abstractmethod
    def update_avatar(self, email, url: str) -> UserOut: ...
