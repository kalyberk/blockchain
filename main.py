from account import Account
import multiprocessing
from multiprocessing.connection import Client


def main():
    input("Creating accounts for Alice and Bob. Press Enter to continue...\n")
    alice = Account()
    print(f"Alice's address: {alice.address}\n")
    bob = Account()
    print(f"Bob's address: {bob.address}\n")

    input("Alice is sending 10 coins to Bob. Press Enter to continue...")
    txn1 = alice.transfer(
        input("Enter Alice's private key: "),
        bob.address,
        10,
        "Alice to Bob",
    )
    print(f"Alice signed. Transaction signature: {txn1.signature}")

    try:
        conn = Client(("localhost", int(input("Enter port of the node: "))))
        conn.send(("enqueue_txn", txn1))
    except:
        print("Connection error")

    # print(f"Alice's balance: {node.state[alice.address]}")
    # print(f"Bob's balance: {node.state[bob.address]}")

    input("Press Enter to exit...")
    conn.send(("disconnect",))
    conn.close()


if __name__ == "__main__":
    main()
