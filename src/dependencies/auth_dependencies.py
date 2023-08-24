from datetime import datetime

from databases.interfaces import Record
from fastapi import Cookie, Depends

from src.services import AuthService
from src.common.exceptions import EmailTaken, RefreshTokenNotValid
from src.schemas.auth_schemas import User as UserSchema


auth_service = AuthService()

async def valid_user_create(user: UserSchema) -> UserSchema:
    if await auth_service.get_user_by_email(user.email):
        print("Hello")
        raise EmailTaken()

    return user


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> Record:
    db_refresh_token = await auth_service.get_refresh_token(refresh_token)
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: Record = Depends(valid_refresh_token),
) -> Record:
    print(refresh_token)
    user = await auth_service.get_user_by_id(refresh_token.user.id)
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: Record) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]
