from typing import Any
from pydantic import RedisDsn, model_validator, MongoDsn
from pydantic_settings import BaseSettings

from src.common.constants import Environment


class Config(BaseSettings):

    DATABASE_URL: MongoDsn

    REDIS_URL: RedisDsn

    SITE_DOMAIN: str = "myapp.com"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    SENTRY_DSN: str | None

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1"

settings = Config()

app_configs: dict[str, Any] = {"title": "App API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutes

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True


auth_config = AuthConfig()