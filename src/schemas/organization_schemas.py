from pydantic import HttpUrl, constr

from src.schemas.base_schema import BaseSchema


class Organization(BaseSchema):
    """
    """

    name: constr(min_length=3, max_length=50)
    description: str
    subdomain: constr(min_length=3, max_length=50)
    website: HttpUrl
    logo_url: HttpUrl


class OrganizationResponse(Organization):
    """
    """

    id: str
