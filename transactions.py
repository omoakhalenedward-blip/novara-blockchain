"""
NOVARA BLOCKCHAIN
Module: Transaction Engine
Version: 1.0.0

Creates, signs, validates and verifies NOVARA transactions.
"""

import hashlib
import json
import time
import math

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PublicKey
)


class Transaction:

    def __init__(self, sender, receiver, amount):

        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()

        self.public_key = None
        self.signature = None

        self.transaction_id = self.generate_id()

    def transaction_data(self):

        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }

    def generate_id(self):

        encoded = json.dumps(
            self.transaction_data(),
            sort_keys=True,
            separators=(",", ":")
        ).encode()

        return hashlib.sha256(encoded).hexdigest()

    def sign_transaction(self, wallet):

        if wallet.address != self.sender:
            raise ValueError(
                "Wallet does not own sender address."
            )

        self.public_key = wallet.public_key_bytes.hex()

        self.transaction_id = self.generate_id()

        self.signature = wallet.sign_message(
            self.transaction_id.encode()
        ).hex()

        return self.signature

    def verify_signature(self):

        try:

            if not self.public_key or not self.signature:
                return False

            public_key_bytes = bytes.fromhex(self.public_key)
            signature_bytes = bytes.fromhex(self.signature)

            # Recalculate the sender address from the public key.
            expected_address = (
                "NVR"
                + hashlib.sha256(
                    public_key_bytes
                ).hexdigest()[:40].upper()
            )

            if expected_address != self.sender:
                return False

            public_key = Ed25519PublicKey.from_public_bytes(
                public_key_bytes
            )

            public_key.verify(
                signature_bytes,
                self.transaction_id.encode()
            )

            return True

        except Exception:
            return False

    def validate(self):

        if not isinstance(self.sender, str):
            return False

        if not isinstance(self.receiver, str):
            return False

        if not self.sender.strip() or not self.receiver.strip():
            return False

        if self.sender == self.receiver:
            return False

        if isinstance(self.amount, bool):
            return False

        if not isinstance(self.amount, (int, float)):
            return False

        if not math.isfinite(self.amount) or self.amount <= 0:
            return False

        if not isinstance(self.timestamp, (int, float)):
            return False

        if not math.isfinite(self.timestamp):
            return False

        return True

    def verify_integrity(self):

        return (
            self.validate()
            and self.transaction_id == self.generate_id()
            and self.verify_signature()
        )

    def to_dict(self):

        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "public_key": self.public_key,
            "signature": self.signature
        }


if __name__ == "__main__":

    print("NOVARA SIGNED TRANSACTION ENGINE")
    print("Version: 1.0.0")
    print("Status: Development prototype")
