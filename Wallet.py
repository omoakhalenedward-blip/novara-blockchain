"""
NOVARA BLOCKCHAIN
Module: Wallet System
Version: 0.2.0

Ed25519 cryptographic wallet foundation.
"""

import hashlib

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey
)

from cryptography.hazmat.primitives import serialization


class NovaraWallet:

    def __init__(self):

        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

        self.public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

        self.address = self.generate_address()

    def generate_address(self):

        address_hash = hashlib.sha256(
            self.public_key_bytes
        ).hexdigest()

        return "NVR" + address_hash[:40].upper()

    def sign_message(self, message):

        if not isinstance(message, bytes):
            raise TypeError("Message must be bytes.")

        return self.private_key.sign(message)

    @staticmethod
    def verify_signature(public_key_bytes, message, signature):

        try:
            public_key = Ed25519PublicKey.from_public_bytes(
                public_key_bytes
            )

            public_key.verify(signature, message)

            return True

        except Exception:
            return False

    def get_wallet_info(self):

        return {
            "address": self.address,
            "public_key": self.public_key_bytes.hex()
        }


if __name__ == "__main__":

    wallet = NovaraWallet()

    message = b"NOVARA WALLET TEST"
    signature = wallet.sign_message(message)

    verification = NovaraWallet.verify_signature(
        wallet.public_key_bytes,
        message,
        signature
    )

    print("NOVARA WALLET 0.2.0")
    print("Wallet Address:", wallet.address)
    print("Public Key:", wallet.public_key_bytes.hex())
    print("Signature Valid:", verification)
