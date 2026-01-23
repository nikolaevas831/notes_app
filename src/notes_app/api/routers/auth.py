from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from notes_app.api.models.user import (
    LoggedInUserResponseSchema,
    RegisterUserResponseSchema,
    UserSchema,
)
from notes_app.api.providers import (
    get_hasher,
    get_token,
    get_tx_manager,
    get_user_repo,
)
from notes_app.application.dto.user import CreateUserDTO
from notes_app.application.exception import (
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
    UsernameNotFoundError,
)
from notes_app.application.interfaces.hasher import HasherInterface
from notes_app.application.interfaces.token import TokenInterface
from notes_app.application.interfaces.txmanager import TxManagerInterface
from notes_app.application.interfaces.user_repo import UserRepoInterface
from notes_app.application.usecases.auth import login as application_login
from notes_app.application.usecases.user import create_user as application_create_user

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserSchema,
    user_repo: Annotated[UserRepoInterface, Depends(get_user_repo)],
    tx_manager: Annotated[TxManagerInterface, Depends(get_tx_manager)],
    hasher: Annotated[HasherInterface, Depends(get_hasher)],
) -> RegisterUserResponseSchema:
    try:
        user_dto = CreateUserDTO(username=user_data.username, password=user_data.password)
        user = await application_create_user(
            user_data=user_dto,
            user_repo=user_repo,
            tx_manager=tx_manager,
            hasher=hasher,
        )
        return RegisterUserResponseSchema(username=user.username)
    except UsernameAlreadyExistsError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT) from err


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: Annotated[UserRepoInterface, Depends(get_user_repo)],
    hasher: Annotated[HasherInterface, Depends(get_hasher)],
    token_service: Annotated[TokenInterface, Depends(get_token)],
) -> LoggedInUserResponseSchema:
    try:
        result_login = await application_login(
            username=form_data.username,
            password=form_data.password,
            user_repo=user_repo,
            hasher=hasher,
            token_service=token_service,
        )
        return LoggedInUserResponseSchema(
            access_token=result_login.access_token, token_type=result_login.token_type
        )
    except UsernameNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Username not found"
        ) from err
    except InvalidCredentialsError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        ) from err
