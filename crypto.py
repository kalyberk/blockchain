import secrets
import hashlib


# Elliptic curve (secp256k1-like) parameters
curve = {
    "p": 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    "a": 0,
    "b": 7,
    "Gx": 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    "Gy": 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    "n": 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
}

word_list = [
    "apple",
    "banana",
    "cherry",
    "date",
    "elderberry",
    "fig",
    "grape",
    "honeydew",
    "kiwi",
    "lemon",
    "mango",
    "nectarine",
    "orange",
    "papaya",
    "quince",
    "raspberry",
    "strawberry",
    "tangerine",
    "watermelon",
]


class Crypto:
    @staticmethod
    def random_mnemonic():
        return " ".join(secrets.choice(word_list) for _ in range(6))

    @staticmethod
    def private_key_from_mnemonic(mnemonic):
        return hex(
            int.from_bytes(
                hashlib.sha256(mnemonic.encode()).digest(),
                byteorder="big",
            )
            % curve["n"]
        )[2:]

    @staticmethod
    def generate_public_key(private_key):
        # convert private key from hex to int for scalar multiplication
        private_key = int(private_key, 16)

        initial_x, initial_y, a, p = curve["Gx"], curve["Gy"], curve["a"], curve["p"]
        x, y = initial_x, initial_y
        # scalar multiplication with double & add algorithm, see more: https://wikipedia.org/wiki/Elliptic_curve_point_multiplication
        # bounce around the curve private key number of times
        for i in range(private_key.bit_length()):
            x, y = Crypto.double_point(x, y, a, p)
            if (private_key >> i) & 1:
                x, y = Crypto.add_points(x, y, initial_x, initial_y, a, p)

        # Uncompressed public key: 04 prefix
        # Compressed public key: just x coordinate with a prefix of 02 (y above x-axis) or 03 (y below x-axis)
        # Compressed public keys are possible because:
        # elliptic curves are symmetric across the x-axis and y coordinate can be derived from x coordinate
        return f"0x04{x:0{64}x}{y:0{64}x}"  # Uncompressed public key

    @staticmethod
    def double_point(x, y, a, p):
        lam = ((3 * x * x) + a) * pow(2 * y, -1, p) % p
        xr = (lam * lam - x - x) % p
        yr = (lam * (x - xr) - y) % p
        return xr, yr

    @staticmethod
    def add_points(x1, y1, x2, y2, a, p):
        if x1 == x2 and y1 == y2:
            return Crypto.double_point(x1, y1, a, p)

        lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        xr = (lam * lam - x1 - x2) % p
        yr = (lam * (x1 - xr) - y1) % p
        return xr, yr

    @staticmethod
    def recover_public_key(signature, data):
        a, b, p, n = curve["a"], curve["b"], curve["p"], curve["n"]
        ## TODO: implement public key recovery from signature
        pass

    @staticmethod
    def keypair(mnemonic=None):
        if mnemonic is None:
            mnemonic = Crypto.random_mnemonic()
        private_key = Crypto.private_key_from_mnemonic(mnemonic)
        public_key = Crypto.generate_public_key(private_key)
        return private_key, public_key

    @staticmethod
    def sign(private_key, value, data):
        return hashlib.sha256(
            bytes.fromhex(private_key)
            + value.to_bytes(32, byteorder="big")
            + data.encode()
        ).hexdigest()

    @staticmethod
    def verify(public_key, value, data, signature):
        return Crypto.sign(public_key, value, data) == signature
