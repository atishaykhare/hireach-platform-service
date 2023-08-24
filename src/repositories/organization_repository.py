from src.repositories.base_repository import BaseRepository
from src.models.organization_models import Organization


class OrganizationRepository(BaseRepository):
    model_class = Organization