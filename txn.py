from crypto import Crypto
from utils import Utils


class Txn:
    def __init__(self, sender, recipient, value, data, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.data = data
        self.signature = signature

    def sign(self, private_key):
        self.signature = Crypto.sign(private_key, self.value, self.data)

    def verify(self, public_key):
        return Crypto.verify(public_key, self.value, self.data, self.signature)

    def __str__(self):
        sender = Utils.format_address(self.sender)
        recipient = Utils.format_address(self.recipient)
        return f"Txn from {sender} to {recipient} for {self.value} coins"
