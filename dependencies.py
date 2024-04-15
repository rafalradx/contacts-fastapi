from src.repository.abstract import AbstractContactRepository, AbstractUserRepository
from src.services.pwd_handler import AbstractPasswordHashHandler, BcryptPasswordHandler
from src.database.db import SessionLocal
from src.repository.contacts import ContactRepository
from src.repository.users import UserRepository
from src.config import settings
from redis import Redis


def get_contacts_repository() -> AbstractContactRepository:
    return ContactRepository(SessionLocal())


def get_users_repository() -> AbstractUserRepository:
    return UserRepository(SessionLocal())


def get_password_handler() -> AbstractPasswordHashHandler:
    return BcryptPasswordHandler()


def get_redis_client() -> Redis:
    return Redis(host=settings.redis_host, port=settings.redis_port, db=0)


# def get_JWT_authorizer() -> AuthWithJWT:
#     return AuthWithJWT(
#         secret_key=settings.jwt_secret_key,
#         algorithm=settings.jwt_algorithm,
#         redis_client=Redis(host=settings.redis_host, port=settings.redis_port, db=0),
#         oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/auth/login"),
#     )
