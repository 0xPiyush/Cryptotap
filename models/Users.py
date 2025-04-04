from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField
from datetime import datetime

class users(Document):
    ip = StringField(unique=True, required=True)
    last_claimed = DateTimeField(required=True, default=datetime.now)

    meta = {
        'indexes': ['ip']
    }
