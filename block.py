class Block:
    def __init__(self, index, prev_hash, data, nonce, txns, hash, timestamp=None):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.nonce = nonce
        self.txns = txns
        self.hash = hash
        self.timestamp = timestamp

    def __str__(self):
        return f"Block {self.index} with hash: {self.hash}"
