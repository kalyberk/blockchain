import random
import hashlib
from crypto import Crypto
from txn import Txn


class Account:
    def __init__(self, private_key=None):
        if private_key is None:
            private_key, _, address = self.generate()
        else:
            public_key = Crypto.generate_public_key(private_key)
            address = self.generate_address(public_key)

        print(f"Account created with private key: {private_key}")
        self.address = address

    def generate(self):
        private_key, public_key = Crypto.keypair()
        address = self.generate_address(public_key)
        return private_key, public_key, address

    @staticmethod
    def generate_address(public_key):
        return hashlib.sha256(public_key.encode()).hexdigest()[-40:]

    def transfer(self, private_key, recipient, value, data):
        txn = Txn(self.address, recipient, value, data)
        txn.sign(private_key)
        return txn
