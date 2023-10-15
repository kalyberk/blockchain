import argparse
import time
import multiprocessing
import threading
from multiprocessing.connection import Listener
from datetime import datetime, timedelta
from crypto import Crypto
from blockchain import Blockchain


class Node:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.mempool = []  # list of transactions
        self.state = {}  # world state of account balances
        self.peers = []  # list of peers
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

    def rpc(self, method, *args):
        methods = {
            "ping": lambda: "pong",
            ## "get_balance": self.get_balance,
            "get_txn": self.get_txn,
            "enqueue_txn": self.enqueue_txn,
            "add_peer": self.add_peer,
        }
        if method in methods:
            return methods[method](*args)
        else:
            raise Exception("Method not found")

    def mine(self):
        data = f"Block at [{datetime.now()}]"
        txns = self.mempool[: self.blockchain.block_size]

        # TODO: implement a proper transaction validation mechanism
        # for txn in txns:
        #     public_key = Crypto.recover_public_key(txn.signature)
        #     if not txn.verify(public_key):
        #         print(f"Invalid txn: {txn.signature}")
        #         txns.remove(txn)

        block = self.blockchain.mine(data, txns)
        print(f"Mined block: {block.hash}")

        self.dequeue_txns(txns)
        self.set_state()

    def handle_connection(self, address):
        listener = Listener(address)
        print(f"Listening on {address}")
        while True:
            conn = listener.accept()
            while True:
                msg = conn.recv()
                if msg == "disconnect":
                    conn.close()
                    break
                else:
                    try:
                        response = self.rpc(*msg)
                        conn.send(response)
                    except Exception as e:
                        conn.send(f"Error: {e}")

    def handle_mining(self):
        print("Mining...")
        while True:
            time.sleep(10)

            last_block = self.blockchain.blocks[-1]
            if datetime.now() - last_block.timestamp > timedelta(seconds=10):
                if len(self.mempool) == 0:
                    print("No txns to mine")
                else:
                    try:
                        block = self.mine()
                    except Exception as e:
                        print(f"Error: {e}")

    def run(self, port):
        mining_thread = threading.Thread(target=self.handle_mining)
        mining_thread.start()

        address = ("localhost", port)
        connection_thread = threading.Thread(
            target=self.handle_connection, args=(address,)
        )
        connection_thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000, help="Port number for node")
    args = parser.parse_args()

    blockchain = Blockchain()
    blockchain.genesis()

    node = Node(blockchain)
    node.run(args.port)
