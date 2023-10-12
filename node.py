import time
import datetime
from multiprocessing import Manager
from blockchain import Blockchain


class Node:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.mempool = Manager().list()  # list of transactions
        self.state = Manager().dict()  # world state of account balances
        self.peers = Manager().list()  # list of peers
        self.set_state()

    def enqueue_txn(self, txn):
        if txn.signature not in [txn.signature for txn in self.mempool]:
            self.mempool.append(txn)
            self.broadcast_txn(txn)

    def dequeue_txn(self, txn):
        if txn.signature in [txn.signature for txn in self.mempool]:
            self.mempool.pop(
                [txn.signature for txn in self.mempool].index(txn.signature)
            )

    def dequeue_txns(self, txns):
        for txn in txns:
            self.dequeue_txn(txn)

    def broadcast_txn(self, txn):
        for peer in self.peers:
            peer.enqueue_txn(txn)

    def get_txn(self, signature):
        for block in self.blockchain.blocks:
            for txn in block.txns:
                if txn.signature == signature:
                    return txn
        return None

    def set_state(self):
        # TODO: implement a proper state sync mechanism
        self.state.clear()

        for block in self.blockchain.blocks:
            for txn in block.txns:
                if txn.sender not in self.state:
                    self.state[txn.sender] = 0
                if txn.recipient not in self.state:
                    self.state[txn.recipient] = 0
                self.state[txn.sender] -= txn.value
                self.state[txn.recipient] += txn.value

        return self.state

    def add_peer(self, peer):
        self.peers.append(peer)

    def sync(self):
        for peer in self.peers:
            if len(peer.blockchain.blocks) > len(self.blockchain.blocks):
                self.blockchain = peer.blockchain

    def run(self):
        print("Node is running")
        while True:
            time.sleep(10)
            if len(self.mempool) > 0:
                data = f"Block at [{datetime.datetime.now()}]"
                txns = self.mempool[: self.blockchain.block_size]
                block = self.blockchain.mine(data, txns)
                print(f"New block mined: {block}")
                self.set_state()
                self.dequeue_txns(txns)
            else:
                print("No txns to mine")

    def wait_for_txn(self, signature):
        while True:
            txn = self.get_txn(signature)
            if txn is not None:
                print(f"Transaction mined: {txn.signature}")
                break
            else:
                print("Waiting for transaction to be mined...")
                time.sleep(5)
