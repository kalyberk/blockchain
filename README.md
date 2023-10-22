# Lightweight blockchain implementation

This blockchain prototype offers a lightweight, demonstrative solution designed to showcase blockchain principles. In contrast to Bitcoin, it employs an account-based structure akin to Ethereum, rather than the UTXO model. Security against Sybil attacks is maintained through a straightforward Proof-of-Work mechanism. To achieve consensus among participating nodes, the protocol employs the longest chain rule. Notably, this blockchain stores data exclusively in memory. Key pair generation, digital signature signing, and verification are all underpinned by elliptic curve cryptography.

## Installation

No external dependencies are required to run the project.

## Usage

Start running a node (port is optional):

```bash
python node.py --port 5001
```

Run the interactive main script to interact with the node:

```bash
python main.py
```
