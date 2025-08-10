from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from notes_app.api.models.user import UserSchema, UserResponseSchema
from notes_app.api.providers import (
    get_user_repo,
    get_tx_manager,
    get_hasher_service,
    get_token_service,
)
from notes_app.application.interfaces.hasher import HasherInterface
from notes_app.application.interfaces.token import TokenInterface
from notes_app.application.interfaces.txmanager import TxManagerInterface
from notes_app.application.interfaces.user_repo import UserRepoInterface
from notes_app.application.usecases.auth import login as application_login
from notes_app.application.exception import (
    UsernameAlreadyExistsError,
    UsernameNotFoundError,
    InvalidCredentialsError,
)
from notes_app.application.usecases.user import create_user as application_create_user

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=201, response_model=UserResponseSchema)
async def register_user(
    user_data: UserSchema,
    user_repo: Annotated[UserRepoInterface, Depends(get_user_repo)],
    tx_manager: Annotated[TxManagerInterface, Depends(get_tx_manager)],
    hasher: Annotated[HasherInterface, Depends(get_hasher_service)],
):
    try:
        user = await application_create_user(
            user_data=user_data,
            user_repo=user_repo,
            tx_manager=tx_manager,
            hasher=hasher,
        )
        user_dict = {"username": user.username}
        return UserResponseSchema(**user_dict)
    except UsernameAlreadyExistsError:
        raise HTTPException(status_code=409)


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: Annotated[UserRepoInterface, Depends(get_user_repo)],
    hasher: Annotated[HasherInterface, Depends(get_hasher_service)],
    token_service: Annotated[TokenInterface, Depends(get_token_service)],
):
    try:
        return await application_login(
            username=form_data.username,
            password=form_data.password,
            user_repo=user_repo,
            hasher=hasher,
            token_service=token_service,
        )
    except UsernameNotFoundError:
        raise HTTPException(status_code=401, detail="Username not found")
    except InvalidCredentialsError:
        raise HTTPException(status_code=400, detail="Incorrect password")
