from fastapi import APIRouter, Depends, status

from src.common.jwt import parse_jwt_user_data
from src.schemas.auth_schemas import JWTData

from src.services import OrganizationService
from src.dependencies.organization_dependencies import valid_organization_create
from src.schemas.organization_schemas import Organization as OrganizationSchema
from src.schemas.organization_schemas import OrganizationResponse

router = APIRouter(prefix="/organization", tags=["Organization"])
organization_service = OrganizationService()


@router.post("/create-organization",
             status_code=status.HTTP_201_CREATED,
             response_model=OrganizationResponse)
async def create_organization(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    organization: OrganizationSchema = Depends(valid_organization_create),
) -> dict[str, str]:

    organization = await organization_service.create_organization(organization)

    return OrganizationResponse(**organization.__dict__())


@router.post("/update-organization",
             status_code=status.HTTP_201_CREATED,
             response_model=OrganizationResponse)
async def update_organization(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    organization: OrganizationSchema = Depends(valid_organization_create),
) -> dict[str, str]:

    organization = await organization_service.update_organization(organization)

    return OrganizationResponse(**organization.__dict__())


@router.get("/get-organization", response_model=OrganizationResponse)
async def get_my_account(
    organization_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:

    organization = await organization_service.get_organization_by_id(organization_id)

    return OrganizationResponse(**organization.__dict__())