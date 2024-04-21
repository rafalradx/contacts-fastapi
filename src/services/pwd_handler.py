from abc import ABC, abstractmethod
import bcrypt


class AbstractPasswordHashHandler(ABC):
    """
    An abstract base class defining the interface for a password hashing handler.

    Concrete implementations of this class must provide implementations for
    the abstract methods defined here.

    """

    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        """
        Generate a hashed password from the provided plain password.

        :param password: The plain password to be hashed.
        :type passwrod: str
        :return: The hashed password.
        :rtype: str

        """
        ...

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify if the provided plain password matches the hashed password.

        :param plain_password: The plain password to be verified.
        :type plain_password: str
        :param hashed_password: The hashed password to be compared against.
        :type hashed_password: str

        :return: True if the plain password matches the hashed password, False otherwise.
        :rtype: bool

        """
        ...


class BcryptPasswordHandler(AbstractPasswordHashHandler):
    """
    A concrete implementation of the AbstractPasswordHashHandler interface
    that uses the bcrypt hashing algorithm.

    """

    def __init__(self, rounds: int = 12):
        """
        Initialize the BcryptPasswordHandler with the specified number of hashing rounds.

        :param rounds: The log2(iterations) of hashing iterations to use (default is 12 => 2^12=4096 iterations) .
        :type rounds: int

        """
        self._rounds = rounds

    def get_password_hash(self, password: str) -> str:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=self._rounds)
        hashed_password_bytes = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        hashed_password = hashed_password_bytes.decode("utf-8")
        return hashed_password

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        password_bytes = plain_password.encode("utf-8")
        hashed_password_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(
            password=password_bytes, hashed_password=hashed_password_bytes
        )
