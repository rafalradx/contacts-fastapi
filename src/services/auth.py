from typing import Optional
import redis as redis
import pickle
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from redis import Redis
from src.config import settings
from src.database.db import get_db
from src.repository import users as repository_users
from src.schemas.users import UserOut
from dependencies import AbstractUserRepository
from abc import ABC, abstractmethod

# ATTENTION!!! bcrypt warning due to passlib which attempts to read a bcrypt version (for logging only)
# passlib seems to be abandoned - considering removing it


class AuthWithJWT:
    # _secret_key = settings.jwt_secret_key
    # _algorithm = settings.jwt_algorithm
    # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    # r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        redis_client: Redis,
        oauth2_scheme: OAuth2PasswordBearer,
        users_repository: AbstractUserRepository,
    ) -> None:
        self._secret_key: str = secret_key
        self._algorithm: str = algorithm
        self._redis_client: Redis = redis_client
        self._oauth2_scheme: OAuth2PasswordBearer = oauth2_scheme
        self._user_repository: AbstractUserRepository = users_repository

    # define a function to generate a new access token
    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        print(to_encode)
        if expires_delta:
            expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.now(timezone.utc), "exp": expire, "scope": "access_token"}
        )
        print(to_encode)
        encoded_access_token = jwt.encode(
            to_encode, self._secret_key, algorithm=self._algorithm
        )
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.now(timezone.utc), "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self._secret_key, algorithm=self._algorithm
        )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token, self._secret_key, algorithms=[self._algorithm]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self,
    ) -> UserOut:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token = Depends(self._oauth2_scheme)
        try:
            # Decode JWT
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        # return email
        # user = self.r.get(f"user:{email}")
        # if user is None:
        ##user = await repository_users.get_user_by_email(email, db)
        user = await self._user_repository.get_user_by_email(email)
        if user is None:
            raise credentials_exception
            # await self.r.set(f"user:{email}", pickle.dumps(user))
            # await self.r.expire(f"user:{email}", 900)
        # else:
        #     user = pickle.loads(user)
        return user

    def create_email_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
        token = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return token

    async def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            )


class HandleJWT:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
    ) -> None:
        self._secret_key: str = secret_key
        self._algorithm: str = algorithm

    # define a function to generate a new access token
    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.now(timezone.utc), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self._secret_key, algorithm=self._algorithm
        )
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.now(timezone.utc), "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self._secret_key, algorithm=self._algorithm
        )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token, self._secret_key, algorithms=[self._algorithm]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    def create_email_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
        token = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return token

    async def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            )

    async def get_email_from_access_token(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        print(token)
        try:
            # Decode JWT
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception
        print(email)
        return email


auth_service = HandleJWT(
    secret_key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
)
