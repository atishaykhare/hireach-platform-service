
from src.services import organization_service
from src.schemas.organization_schemas import Organization as OrganizationSchema
from src.common.exceptions import NameTaken


async def valid_organization_create(organization: OrganizationSchema) -> OrganizationSchema:
    if await organization_service.get_organization_by_name(organization.name):
        raise NameTaken()

    return organization