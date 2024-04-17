from src.repository.abstract import AbstractContactRepository, AbstractUserRepository
from src.services.pwd_handler import AbstractPasswordHashHandler, BcryptPasswordHandler
from src.database.db import SessionLocal
from src.repository.contacts import ContactRepository
from src.repository.users import UserRepository
from src.config import settings
from redis.asyncio import Redis


def get_contacts_repository() -> AbstractContactRepository:
    return ContactRepository(SessionLocal())


def get_users_repository() -> AbstractUserRepository:
    return UserRepository(SessionLocal())


def get_password_handler() -> AbstractPasswordHashHandler:
    return BcryptPasswordHandler()


def get_redis_client() -> Redis:
    Redis()
    return Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
