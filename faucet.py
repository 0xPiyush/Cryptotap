from datetime import datetime
import json
from mongoengine import connect
from mongoengine.errors import DoesNotExist, NotUniqueError
from models.Users import users
from models.Wallets import wallets
from datetime import datetime
import random


class Faucet:
    def __init__(self, config_json: str, db_uri: str):
        self.config_json = config_json
        self.db_uri = db_uri
        # Load Config
        self.config = self._load_config(self.config_json)
        # Connect to Mongodb
        self.db_connect(self.db_uri)

    def claim(self, request_ip, wallet_addr, coin, net):
        claim_amount = self._claim_amount(coin)
        try:
            users(ip=request_ip).save()
            try:
                wallets(wallet_addr=wallet_addr, wallet_type=coin, network=net, balance=claim_amount).save()
            except NotUniqueError:
                existing_wallet = wallets.objects(wallet_addr=wallet_addr, wallet_type=coin, network=net)[0]
                existing_wallet.balance += claim_amount
                existing_wallet.save()

        except NotUniqueError:
            existing_user = users.objects(ip=request_ip)[0]
            last_claimed = existing_user.last_claimed
            can_claim = self._can_claim(last_claimed, coin)
            if type(can_claim) == tuple:
                return False, can_claim[1]
            try:
                wallets(wallet_addr=wallet_addr, wallet_type=coin, network=net, balance=claim_amount).save()
                existing_user.last_claimed = datetime.now()
                existing_user.save()
            except NotUniqueError:
                existing_wallet = wallets.objects(wallet_addr=wallet_addr, wallet_type=coin, network=net)[0]
                existing_wallet.balance += claim_amount
                existing_wallet.save()
                existing_user.last_claimed = datetime.now()
                existing_user.save()
        return True, claim_amount

    def wallet_info(self, wallet_addr, coin, net):
        try:
            return wallets.objects(wallet_addr=wallet_addr, wallet_type=coin, network=net)[0]
        except DoesNotExist:
            return False

    def get_config(self, coin):
        return self.config[coin]
                    

    def _can_claim(self, last_claimed, coin):
        claim_timeout = self.config[coin]['claim_timeout']
        if (datetime.now() - last_claimed).seconds >= claim_timeout:
            return True
        time_left = claim_timeout - (datetime.now() - last_claimed).seconds
        return False, time_left

    def _claim_amount(self, coin):
        return random.uniform(self.config[coin]['prize_min'], self.config[coin]['prize_max'])

    def db_connect(self, db_uri: str):
        connect(host=db_uri)

    def _load_config(self, config_json: str):
        with open(config_json, 'r') as f:
            config = json.load(f)
        return config
