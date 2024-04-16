from abc import ABC, abstractmethod
import bcrypt


class AbstractPasswordHashHandler(ABC):
    @abstractmethod
    def get_password_hash(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...


class BcryptPasswordHandler(AbstractPasswordHashHandler):
    def __init__(self, rounds: int = 12):
        self._rounds = rounds

    def get_password_hash(self, password: str):
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=self._rounds)
        hashed_password_bytes = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        hashed_password = hashed_password_bytes.decode("utf-8")
        return hashed_password

    def verify_password(self, plain_password: str, hashed_password: str):
        password_bytes = plain_password.encode("utf-8")
        hashed_password_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(
            password=password_bytes, hashed_password=hashed_password_bytes
        )
