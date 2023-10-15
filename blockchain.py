import datetime
import hashlib
from block import Block
from account import Account
from txn import Txn


class Blockchain:
    def __init__(self):
        self.blocks = []
        self.difficulty = 3  # number of leading zeros in the block hash
        self.block_size = 5  # number of txns per block

    def genesis(self):
        if len(self.blocks) > 0:
            return

        data = "Dallama block"
        txns = []
        prev_hash = "0" * 64
        nonce, hash = self.pow(0, prev_hash, data, txns)
        block = Block(0, prev_hash, data, nonce, txns, hash, datetime.datetime.now())
        self.blocks.append(block)

    def hash(self, index, prev_hash, data, nonce, txns):
        value = (
            str(index) + str(prev_hash) + str(data) + str(nonce) + str(txns)
        ).encode("utf-8")
        return hashlib.sha256(value).hexdigest()

    def pow(self, index, prev_hash, data, txns):
        nonce = 0
        while True:
            hash = self.hash(index, prev_hash, data, nonce, txns)
            if hash.startswith("0" * self.difficulty):
                return nonce, hash
            else:
                nonce += 1

    def mine(self, data, txns):
        last_block = self.blocks[-1]
        index = last_block.index + 1
        prev_hash = last_block.hash
        nonce, hash = self.pow(index, prev_hash, data, txns)
        block = Block(
            index, prev_hash, data, nonce, txns, hash, datetime.datetime.now()
        )
        self.blocks.append(block)
        return block

    def __str__(self):
        return f"Blockchain with difficulty: {self.difficulty} and # of blocks: {len(self.blocks)}"

    zero_address = lambda self: "0" * 40
