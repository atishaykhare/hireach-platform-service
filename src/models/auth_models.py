from mongoengine import EmailField
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import DateTimeField
from mongoengine import ReferenceField

from src.models.base_model import BaseDocument


class User(BaseDocument):
    """
    """

    email = EmailField(required=True, unique=True)
    name = StringField(required=True)
    password = StringField(required=True)
    is_admin = BooleanField(required=True, default=False)


class RefreshToken(BaseDocument):
    """
    """

    user = ReferenceField(User)
    refresh_token = StringField(required=True)
    expires_at = DateTimeField(required=True)
