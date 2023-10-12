import random
import hashlib
from crypto import Crypto
from txn import Txn


class Account:
    def __init__(self):
        (
            self.private_key,  # store it only for demo purposes (to prevent inputting it every time)
            self.public_key,
            self.address,
        ) = self.generate()

    def generate(self):
        private_key, public_key = Crypto.keypair()
        address = self.generate_address(public_key)
        # return public_key, address
        return private_key, public_key, address

    @staticmethod
    def generate_address(public_key):
        return hashlib.sha256(public_key.encode()).hexdigest()[-40:]

    def transfer(self, private_key, recipient, value, data):
        txn = Txn(self.address, recipient, value, data)
        txn.sign(private_key)
        return txn
