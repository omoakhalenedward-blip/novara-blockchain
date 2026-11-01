"""
NOVARA BLOCKCHAIN
Module: Wallet System
Version: 0.1.0

Generates cryptographic wallet keys and addresses.
"""

import hashlib
import secrets


class NovaraWallet:

    def __init__(self):
        self.private_key = secrets.token_bytes(32)
        self.public_key = self.generate_public_key()
        self.address = self.generate_address()

    def generate_public_key(self):
        # Prototype only: placeholder public key.
        # Production wallets must use real asymmetric cryptography.
        return hashlib.sha256(self.private_key).hexdigest()

    def generate_address(self):
        address_hash = hashlib.sha256(
            self.public_key.encode()
        ).hexdigest()

        return "NVR" + address_hash[:40].upper()

    def get_wallet_info(self):
        return {
            "address": self.address,
            "public_key": self.public_key
        }


if __name__ == "__main__":

    wallet = NovaraWallet()

    print("================================")
    print("       NOVARA WALLET")
    print("================================")

    print("Wallet Address:", wallet.address)
    print("Public Key:", wallet.public_key)
    print("Wallet Status: CREATED")
