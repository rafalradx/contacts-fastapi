from abc import ABC, abstractmethod
from src.schemas.contacts import ContactIn, ContactOut
from src.schemas.users import UserOut


class AbstractContactRepository(ABC):

    @abstractmethod
    def get_contact(self, id, current_user: UserOut) -> ContactOut: ...

    @abstractmethod
    def get_contacts(self, current_user: UserOut) -> list[ContactOut]: ...

    @abstractmethod
    def create_contact(
        self, contact: ContactIn, current_user: UserOut
    ) -> ContactOut: ...

    @abstractmethod
    def delete_contact(self, id, current_user: UserOut) -> ContactOut: ...

    @abstractmethod
    def update_contact(
        self, id, contact: ContactIn, current_user: UserOut
    ) -> ContactOut: ...
