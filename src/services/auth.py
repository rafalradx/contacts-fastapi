from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from src.config import settings


class HandleJWT:
    """
    Class to handle JSON Web Tokens (JWT).

    :param secret_key: The secret key used to sign the tokens.
    :type secret_key: str

    :param algorithm: The algorithm used for token signing.
    :type algorithm: str
    """

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
        """
        Generate a new access token.

        :param data: The payload data to include in the token.
        :type data: dict

        :param expires_delta: Optional. The expiration time delta in seconds.
        :type expires_delta: Optional[float]

        :return: The encoded access token.
        :rtype: str
        """
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
        """
        Generate a new refresh token.

        :param data: The payload data to include in the token.
        :type data: dict

        :param expires_delta: Optional. The expiration time delta in seconds.
        :type expires_delta: Optional[float]

        :return: The encoded refresh token.
        :rtype: str
        """
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
        """
        Decode and verify a refresh token.

        :param refresh_token: The refresh token to decode.
        :type refresh_token: str

        :return: The email address extracted from the token.
        :rtype: str

        :raises HTTPException: If the token is invalid or has an invalid scope.
        """
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
        """
        Generate a new token for email verification.

        :param data: The payload data to include in the token.
        :type data: dict

        :return: The encoded email verification token.
        :rtype: str
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
        token = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return token

    async def get_email_from_token(self, token: str):
        """
        Extract the email address from an email verification token.

        :param token: The email verification token.
        :type token: str

        :return: The email address extracted from the token.
        :rtype: str

        :raises HTTPException: If the token is invalid.
        """
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
        """
        Extract the email address from an access token.

        :param token: The access token.
        :type token: str

        :return: The email address extracted from the token.
        :rtype: str

        :raises HTTPException: If the token is invalid or has an invalid scope.
        """
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
        return email


auth_service = HandleJWT(
    secret_key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
)
