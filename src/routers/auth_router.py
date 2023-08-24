from databases.interfaces import Record
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status, Security
from typing import Annotated

from src.dependencies.auth_dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create
)
from src.common.jwt import parse_jwt_user_data
from src.common.jwt import create_access_token
from src.schemas.auth_schemas import LoginResponse
from src.schemas.auth_schemas import User as UserSchema
from src.schemas.auth_schemas import JWTData
from src.schemas.auth_schemas import UserResponse, UserAuth
from src.services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/create-user",
             status_code=status.HTTP_201_CREATED,
             response_model=UserResponse)
async def register_user(
    auth_data: UserSchema = Depends(valid_user_create),
) -> dict[str, str]:

    user = await auth_service.create_user(auth_data)

    return UserResponse.model_validate(user)


@router.get("/get-user-details", response_model=UserResponse)
async def get_my_account(
    jwt_data: Annotated[JWTData, Security(parse_jwt_user_data)]
) -> dict[str, str]:

    user = await auth_service.get_user_by_id(jwt_data.user_id)

    return UserResponse.model_validate(user)


@router.post("/login", response_model=LoginResponse)
async def auth_user(auth_data: UserAuth, response: Response) -> LoginResponse:
    user = await auth_service.authenticate_user(auth_data)
    refresh_token_value = await auth_service.create_refresh_token(
        user_id=user["id"])

    response.set_cookie(
        **auth_service.get_refresh_token_settings(refresh_token_value))

    return LoginResponse(
        access_token=create_access_token(user=user),
        refresh_token=refresh_token_value,
        user=UserResponse.model_validate(user)
    )


@router.put("/refresh-tokens", response_model=LoginResponse)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: Record = Depends(valid_refresh_token),
    user: Record = Depends(valid_refresh_token_user),
) -> LoginResponse:
    refresh_token_value = await auth_service.create_refresh_token(
        user_id=user["id"]
    )
    response.set_cookie(
        **auth_service.get_refresh_token_settings(refresh_token_value))

    worker.add_task(auth_service.expire_refresh_token, refresh_token["id"])
    return LoginResponse(
        access_token=create_access_token(user=user),
        refresh_token=refresh_token_value,
        user=UserResponse.model_validate(user),
    )


@router.delete("/logout")
async def logout_user(
    response: Response,
    refresh_token: Record = Depends(valid_refresh_token),
) -> None:
    await auth_service.expire_refresh_token(refresh_token["id"])

    response.delete_cookie(
        **auth_service.get_refresh_token_settings(
            refresh_token["refresh_token"], expired=True)
    )