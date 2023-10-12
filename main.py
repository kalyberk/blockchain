from account import Account
from node import Node
from blockchain import Blockchain
from multiprocessing import Process, Manager
import time


def main():
    with Manager() as manager:
        blockchain = Blockchain()
        blockchain.genesis()
        print(f"New blockchain: {blockchain}")
        print(f"Genesis block: {blockchain.blocks[0]}")
        print(f"Genesis txn: {blockchain.blocks[0].txns[0]}")

        node = Node(blockchain)
        node_process = Process(target=node.run, args=(), daemon=True)
        node_process.start()

        alice = Account()
        print(f"Alice's address: {alice.address}")
        bob = Account()
        print(f"Bob's address: {bob.address}")

        # Send some coins to Alice from Satoshi
        # Get satoshi's account
        satoshi = Account()

        print("Alice wants to send coins to Bob")
        txn1 = alice.transfer(
            alice.private_key,
            bob.address,
            10,
            "Alice to Bob",
        )
        print(f"Alice signed. Transaction signature: {txn1.signature}")

        # Publish transaction to the network via node
        node.enqueue_txn(txn1)

        # Wait for transaction to be mined
        wait_txn1_process = Process(target=node.wait_for_txn, args=(txn1.signature,))
        wait_txn1_process.start()
        wait_txn1_process.join()

        # Check balances
        print(f"Alice's balance: {node.state[alice.address]}")
        print(f"Bob's balance: {node.state[bob.address]}")

        node_process.join()


if __name__ == "__main__":
    main()
