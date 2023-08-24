from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import BooleanField

from datetime import datetime


class BaseDocument(Document):
    created_by = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_by = StringField(required=True)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    is_deleted = BooleanField(default=False)

    meta = {
        'abstract': True
    }