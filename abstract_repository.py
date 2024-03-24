from abc import ABC, abstractmethod
from models import ContactIn, ContactOut


class AbstractContactRepository(ABC):

    @abstractmethod
    def get_note(self, id) -> ContactOut: ...

    @abstractmethod
    def get_notes(self) -> list[ContactOut]: ...

    @abstractmethod
    def create_note(self, contact: ContactIn) -> ContactOut: ...
