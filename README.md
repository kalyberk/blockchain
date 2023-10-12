# Lightweight blockchain implementation

A lightweight blockchain implementation written in Python, only for demonstration purposes. It is not UTXO-based like Bitcoin, but account-based like Ethereum. A simple PoW (Proof-of-Work) mechanism secures the network by preventing Sybil attacks. To ensure the consensus between nodes, the longest chain rule is used. The blockchain data is not stored persistently, but only in memory. Elliptic curve cryptography is used for the keypair generation and the digital signature signing and verification.

## Installation

No dependencies are required to run the project. You may run the project in a virtual environment, but it is not necessary. Depending on your OS and global Python version, you may want to use [pyenv] to install a specific Python version.

## Usage

Run:

```bash
python main.py
```

<!-- ## Installation

There are numerous ways to setup Python projects. In this project, [pyenv] and [pipenv] are utilized to manage the Python version and the dependencies. If these tools are not installed yet, [homebrew] may be used to install them.

```bash
brew install pyenv pipenv
```

Any Python version can be installed with pyenv. To install Python 3.8.0 and set it as the local version:

```bash
pyenv install 3.10.0
pyenv local 3.10.0
```

Create the virtual environment with pipenv:

```bash
pipenv install
```

Or if you have not set the Python version with pyenv:

```bash
pipenv --python 3.10.0
```

There is no need the activate the virtual environment since pipenv does it under the hood.

## Usage

Start the blockchain and run:

```bash
pipenv run python main.py
``` -->

[pyenv]: https://github.com/pyenv/pyenv
[pipenv]: https://pypi.org/project/pipenv
[homebrew]: https://brew.sh
