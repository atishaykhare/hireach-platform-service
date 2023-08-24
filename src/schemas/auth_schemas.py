import re
from pydantic import EmailStr, Field, validator, ConfigDict, AliasChoices
from typing import Optional
from src.schemas.base_schema import BaseSchema


STRONG_PASSWORD_PATTERN = \
    re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class User(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    name: str
    organization_id: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_name": "Test User",
                    "password": "Password@123",
                    "email": "test@test.com",
                }
            ]
        }
    }

    @validator("password")
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password


class UserResponse(BaseSchema):
    user_id: str = Field(alias=AliasChoices("id", "user_id"))
    email: EmailStr
    name: str


class UserAuth(BaseSchema):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "test@test.com",
                    "password": "Password@123",
                }
            ]
        }
    }


class JWTData(BaseSchema):
    user_id: str = Field(alias="sub")
    is_admin: bool = False


class LoginResponse(BaseSchema):
    model_config = ConfigDict(extra="allow")
    access_token: str
    refresh_token: str
    user: UserResponse
