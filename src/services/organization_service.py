
from databases.interfaces import Record

from src.schemas.organization_schemas import Organization as OrganizationSchema
from src.repositories import OrganizationRepository


class OrganizationService:
    """
    """

    async def create_organization(
            self, organization: OrganizationSchema) -> Record | None:
        """
        """

        return OrganizationRepository.create(
            **organization.dict(),
            created_by='',
            updated_by='',
        )


    def get_organization_by_id(self, organization_id: str) -> Record | None:
        """
        """

        return OrganizationRepository.get(id=organization_id)

    def get_organization_by_name(self, name: str) -> Record | None:
        """
        """

        return OrganizationRepository.get(name=name)


    def update_organization(self, organization: OrganizationSchema) -> Record | None:
        """
        """

        organization_model = self.get_organization_by_id(organization.id)

        res = OrganizationRepository.update(
            organization_model,
        )

        return res
