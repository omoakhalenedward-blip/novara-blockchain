"""
NOVARA BLOCKCHAIN
Module: Transaction Engine
Version: 0.2.0

Creates, validates and verifies NOVARA transactions.
"""

import hashlib
import json
import time
import math


class Transaction:

    def __init__(self, sender, receiver, amount):

        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()

        self.transaction_id = self.generate_id()

    def generate_id(self):

        transaction_data = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }

        encoded_data = json.dumps(
            transaction_data,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

        return hashlib.sha256(encoded_data).hexdigest()

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

        if not math.isfinite(self.timestamp):
            return False

        return True

    def verify_integrity(self):

        return (
            self.validate()
            and self.transaction_id == self.generate_id()
        )

    def to_dict(self):

        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }


if __name__ == "__main__":

    transaction = Transaction(
        "NOVARA_WALLET_A",
        "NOVARA_WALLET_B",
        10
    )

    print("NOVARA TRANSACTION ENGINE")
    print("=========================")
    print("Transaction:", transaction.to_dict())
    print("Valid:", transaction.validate())
    print("Integrity:", transaction.verify_integrity())
