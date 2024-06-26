from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from fastapi.requests import Request
from src.repository.abstract import AbstractUserRepository
from dependencies import get_users_repository, get_password_handler

from src.schemas.users import UserIn, UserOut, Token, RequestEmail
from src.services.auth import auth_service
from src.services.pwd_handler import AbstractPasswordHashHandler
from src.services.email import send_email
from src.config import settings

EMAIL_VERIFICATION_REQUIRED = settings.email_verification

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    new_user: UserIn,
    background_tasks: BackgroundTasks,
    request: Request,
    users_repository: AbstractUserRepository = Depends(get_users_repository),
    pwd_handler: AbstractPasswordHashHandler = Depends(get_password_handler),
) -> UserOut:
    """
    Endpoint to register a new user.

    :param new_user: The user details to be registered.
    :type new_user: UserIn

    :param background_tasks: Background tasks to be executed.
    :type background_tasks: BackgroundTasks

    :param request: The incoming request.
    :type request: Request

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param pwd_handler: The password hashing handler.
    :type pwd_handler: AbstractPasswordHashHandler

    :return: The registered user details.
    :rtype: UserOut

    :raises HTTPException 409: If the account already exists.
    """
    exist_user = await users_repository.get_user_by_email(new_user.email)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    new_user.password = pwd_handler.get_password_hash(new_user.password)
    new_user = await users_repository.create_user(new_user)

    if EMAIL_VERIFICATION_REQUIRED:
        background_tasks.add_task(
            send_email, new_user.email, new_user.username, request.base_url
        )
    return new_user


@router.post("/login")
async def login(
    login_form: OAuth2PasswordRequestForm = Depends(),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
    pwd_handler: AbstractPasswordHashHandler = Depends(get_password_handler),
) -> Token:
    """
    Endpoint for user login.

    :param login_form: The login form containing username (email) and password.
    :type login_form: OAuth2PasswordRequestForm

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param pwd_handler: The password hashing handler.
    :type pwd_handler: AbstractPasswordHashHandler

    :param auth_service: The JWT handling service.
    :type auth_service: HandleJWT

    :return: The generated access and refresh tokens.
    :rtype: Token

    :raises HTTPException 401: If the email, password, or email verification is invalid.
    """
    # confusing! email address is a username in body of login request
    user = await users_repository.get_user_by_email(login_form.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if EMAIL_VERIFICATION_REQUIRED:
        if not user.confirmed:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
            )
    if not pwd_handler.verify_password(login_form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await users_repository.update_token(user, refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/refresh_token")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
) -> Token:
    """
    Endpoint to refresh the access token using the refresh token.

    :param credentials: The HTTP Authorization Credentials containing the refresh token.
    :type credentials: HTTPAuthorizationCredentials

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param auth_service: The JWT handling service.
    :type auth_service: HandleJWT

    :return: The generated access and refresh tokens.
    :rtype: Token

    :raises HTTPException 401: If the refresh token is invalid.
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await users_repository.get_user_by_email(email)
    if user.refresh_token != token:
        await users_repository.update_token(user, None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await users_repository.update_token(user, refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/confirm_email/{token}")
async def confirm_email(
    token: str,
    users_repository: AbstractUserRepository = Depends(get_users_repository),
):
    """
    Endpoint to confirm the email address using the verification token.

    :param token: The verification token.
    :type token: str

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param auth_service: The JWT handling service.
    :type auth_service: HandleJWT

    :return: A message indicating the confirmation status.
    :rtype: dict

    :raises HTTPException 400: If there is a verification error.
    """
    email = await auth_service.get_email_from_token(token)
    user = await users_repository.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await users_repository.confirm_email(email)
    return {"message": "Email confirmed"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    users_repository: AbstractUserRepository = Depends(get_users_repository),
):
    """
    Endpoint to request sending an amail address verifacion email.

    :param body: The request body containing the email address to be confirmed.
    :type body: RequestEmail

    :param background_tasks: Background tasks to be executed.
    :type background_tasks: BackgroundTasks

    :param request: The incoming request.
    :type request: Request

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :return: A message indicating the result of the request.
    :rtype: dict
    """
    if not EMAIL_VERIFICATION_REQUIRED:
        return {"message": "Email verification not required"}

    user = await users_repository.get_user_by_email(body.email)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, request.base_url
        )
    return {"message": "Check your email for confirmation."}
