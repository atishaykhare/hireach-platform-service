from mongoengine import StringField
from mongoengine import URLField

from src.models.base_model import BaseDocument


class Organization(BaseDocument):
    """
    """

    name = StringField(required=True)
    description = StringField()
    subdomain = StringField(required=True)
    website = StringField(required=True)
    logo_url = URLField(required=True)
