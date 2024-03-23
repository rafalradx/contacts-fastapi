import abc

from models import NoteIn, NoteOut


class AbstractNoteRepository(abc.ABC):

    @abc.abstractmethod
    def get_note(self, id) -> NoteOut:
        ...

    @abc.abstractmethod
    def get_notes(self) -> list[NoteOut]:
        ...

    @abc.abstractmethod
    def create_note(self, note: NoteIn) -> NoteOut:
        ...
