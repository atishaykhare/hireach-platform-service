from datetime import datetime, timedelta
from databases.interfaces import Record
from mongoengine import DoesNotExist
from typing import Any

from src.common.utils import generate_random_alphanum
from src.common.config import auth_config
from src.common.security import check_password
from src.common.security import hash_password
from src.common.config import auth_config
from src.common.config import settings
from src.common.exceptions import InvalidCredentials
from src.common.exceptions import NotFound

from src.schemas.auth_schemas import User as UserSchema

from src.models.auth_models import RefreshToken

from src.repositories import UserRepository
from src.repositories import RefreshTokenRepository


class AuthService:

    async def create_user(self, user: UserSchema) -> Record | None:
        """
        """

        hashed_password = hash_password(user.password)

        return UserRepository.create(
            email=user.email,
            password=hashed_password,
            name=user.name,
            created_by='',
            updated_by='',
        )

    async def get_user_by_id(self, user_id: str) -> Record | None:
        """
        """

        try:
            return UserRepository.get(id=user_id)

        except DoesNotExist:
            return None

    async def get_user_by_email(self, email: str) -> Record | None:
        """
        """
        try:
            return UserRepository.get(email=email)

        except DoesNotExist:
            return None

    async def create_refresh_token(
        self, *, user_id: str, refresh_token: str | None = None
    ) -> str:
        """
        """

        if not refresh_token:
            refresh_token = generate_random_alphanum(64)

        user = UserRepository.get(id=user_id)

        refresh_token_db = RefreshToken(
            user=user,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + \
                timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
            created_by='',
            updated_by='',
        )

        refresh_token_db.save()

        return refresh_token

    async def get_refresh_token(self, refresh_token: str) -> Record | None:
        """
        """

        return RefreshTokenRepository.get(refresh_token=refresh_token)


    async def expire_refresh_token(self, refresh_token_id: str) -> None:
        expires_at=datetime.utcnow() - timedelta(days=1)

        refresh_token = RefreshTokenRepository.get(id=refresh_token_id)
        RefreshTokenRepository.update(refresh_token, expires_at=expires_at)

    async def authenticate_user(self, auth_data: UserSchema) -> Record:
        user = await self.get_user_by_email(auth_data.email)

        if not user:
            raise InvalidCredentials()

        if not check_password(auth_data.password, user["password"]):
            raise InvalidCredentials()

        return user

    def get_refresh_token_settings(
        self,
        refresh_token: str,
        expired: bool = False,
    ) -> dict[str, Any]:
        base_cookie = {
            "key": auth_config.REFRESH_TOKEN_KEY,
            "httponly": True,
            "samesite": "none",
            "secure": auth_config.SECURE_COOKIES,
            "domain": settings.SITE_DOMAIN,
        }
        if expired:
            return base_cookie

        return {
            **base_cookie,
            "value": refresh_token,
            "max_age": auth_config.REFRESH_TOKEN_EXP,
        }
