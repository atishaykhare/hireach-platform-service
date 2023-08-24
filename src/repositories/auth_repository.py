from src.repositories.base_repository import BaseRepository
from src.models.auth_models import User
from src.models.auth_models import RefreshToken


class UserRepository(BaseRepository):
    model_class = User


class RefreshTokenRepository(BaseRepository):
    model_class = RefreshToken
