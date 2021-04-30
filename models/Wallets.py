from mongoengine import Document
from mongoengine.fields import DateTimeField, FloatField, StringField
from datetime import datetime


class wallets(Document):
    wallet_addr = StringField(unique=True, require=True)
    wallet_type = StringField(required=True)
    network = StringField(required=True, default='mainnet')
    balance = FloatField(required=True, default=0)
    last_claimed = DateTimeField(required=True, default=datetime.now)

    meta = {
        'indexes': ['wallet_addr', 'wallet_type', 'network']
    }