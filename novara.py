"""
NOVARA BLOCKCHAIN
Version: 0.8.0

Blockchain with Transaction Integrity Verification.
"""

import hashlib
import json
import time
import math

from mempool import NovaraMempool
from transactions import Transaction


class NovaraBlockchain:

    def __init__(self):

        self.chain = []
        self.mempool = NovaraMempool()

        self.create_block([])

    def calculate_hash(self, block):

        contents = {
            key: value
            for key, value in block.items()
            if key != "hash"
        }

        encoded = json.dumps(
            contents,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

        return hashlib.sha256(encoded).hexdigest()

    def create_block(self, transactions):

        previous_hash = (
            self.chain[-1]["hash"]
            if self.chain else "0"
        )

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "transactions": transactions,
            "previous_hash": previous_hash
        }

        block["hash"] = self.calculate_hash(block)

        self.chain.append(block)

        return block

    def verify_transaction(self, transaction_data):

        try:

            if not isinstance(transaction_data, dict):
                return False

            required_fields = {
                "transaction_id",
                "sender",
                "receiver",
                "amount",
                "timestamp",
                "public_key",
                "signature"
            }

            if not required_fields.issubset(transaction_data):
                return False

            transaction = Transaction(
                transaction_data["sender"],
                transaction_data["receiver"],
                transaction_data["amount"]
            )

            transaction.timestamp = transaction_data["timestamp"]
            transaction.transaction_id = transaction_data["transaction_id"]
            transaction.public_key = transaction_data["public_key"]
            transaction.signature = transaction_data["signature"]

            return transaction.verify_integrity()

        except Exception:
            return False

    def add_pending_transaction(self, transaction):

        return self.mempool.add_transaction(transaction)

    def mine_pending_transactions(self):

        if self.mempool.get_transaction_count() == 0:
            return None

        transactions = self.mempool.get_pending_transactions()

        block = self.create_block(transactions)

        self.mempool.clear_mempool()

        return block

    def verify_chain(self):

        if not self.chain:
            return False

        required_fields = {
            "index",
            "timestamp",
            "transactions",
            "previous_hash",
            "hash"
        }

        seen_transaction_ids = set()

        try:

            for i, block in enumerate(self.chain):

                if not isinstance(block, dict):
                    return False

                if not required_fields.issubset(block.keys()):
                    return False

                if block["index"] != i + 1:
                    return False

                if (
                    isinstance(block["timestamp"], bool)
                    or not isinstance(block["timestamp"], (int, float))
                    or not math.isfinite(block["timestamp"])
                ):
                    return False

                if not isinstance(block["transactions"], list):
                    return False

                if not isinstance(block["previous_hash"], str):
                    return False

                if block["hash"] != self.calculate_hash(block):
                    return False

                if i == 0:

                    if block["previous_hash"] != "0":
                        return False

                    if block["transactions"] != []:
                        return False

                else:

                    if block["previous_hash"] != self.chain[i - 1]["hash"]:
                        return False

                for transaction in block["transactions"]:

                    if not self.verify_transaction(transaction):
                        return False

                    transaction_id = transaction["transaction_id"]

                    if transaction_id in seen_transaction_ids:
                        return False

                    seen_transaction_ids.add(transaction_id)

            return True

        except Exception:
            return False

    def save_chain(self, filename="novara_chain.json"):

        if not self.verify_chain():
            raise ValueError("Cannot save invalid blockchain.")

        with open(filename, "w") as file:
            json.dump(self.chain, file, indent=4)

        print("NOVARA blockchain saved successfully.")

    def load_chain(self, filename="novara_chain.json"):

        with open(filename, "r") as file:
            loaded_chain = json.load(file)

        if not isinstance(loaded_chain, list):
            return False

        original_chain = self.chain
        self.chain = loaded_chain

        if self.verify_chain():

            print("NOVARA blockchain loaded successfully.")
            return True

        self.chain = original_chain

        print("Invalid blockchain file.")

        return False


if __name__ == "__main__":

    novara = NovaraBlockchain()

    print("==============================")
    print("NOVARA BLOCKCHAIN 0.8.0")
    print("==============================")

    print("Blockchain valid:", novara.verify_chain())
