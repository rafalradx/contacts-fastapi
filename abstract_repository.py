from abc import ABC, abstractmethod
from models import ContactIn, ContactOut


class AbstractContactRepository(ABC):

    @abstractmethod
    def get_contact(self, id) -> ContactOut: ...

    @abstractmethod
    def get_contacts(self) -> list[ContactOut]: ...

    @abstractmethod
    def create_contact(self, contact: ContactIn) -> ContactOut: ...

    @abstractmethod
    def delete_contact(self, id) -> ContactOut: ...

    @abstractmethod
    def update_contact(self, id, contact: ContactIn) -> ContactOut: ...
