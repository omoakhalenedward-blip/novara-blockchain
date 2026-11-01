"""
NOVARA BLOCKCHAIN
Version: 0.9.0

Balance-Aware Blockchain Engine.
"""

import hashlib
import json
import time
import math

from mempool import NovaraMempool
from transactions import Transaction
from balances import NovaraBalances


class NovaraBlockchain:

    def __init__(self, genesis_allocations):

        if not isinstance(genesis_allocations, dict):
            raise ValueError("Genesis allocations must be a dictionary.")

        if not genesis_allocations:
            raise ValueError("Genesis allocations cannot be empty.")

        self.chain = []
        self.mempool = NovaraMempool()
        self.genesis_allocations = dict(genesis_allocations)

        ledger = NovaraBalances()

        if not ledger.initialize_genesis(self.genesis_allocations):
            raise ValueError("Invalid genesis allocations.")

        self.create_genesis_block()

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

    def create_genesis_block(self):

        block = {
            "index": 1,
            "timestamp": time.time(),
            "transactions": [],
            "previous_hash": "0",
            "genesis_allocations": self.genesis_allocations
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
        def_rebuild_balances(self):

        if not self.chain:
            return None

        genesis = self.chain[0]
        allocations = genesis.get("genesis_allocations")

        if not isinstance(allocations, dict) or not allocations:
            return None

        ledger = NovaraBalances()

        if not ledger.initialize_genesis(allocations):
            return None

        for block in self.chain[1:]:

            for transaction in block["transactions"]:

                if not ledger.apply_transaction(transaction):
                    return None

        return ledger

    def add_pending_transaction(self, transaction):

        try:

            if not isinstance(transaction, Transaction):
                return False

            transaction_data = transaction.to_dict()

            if not self.verify_transaction(transaction_data):
                return False

            ledger = self._rebuild_balances()

            if ledger is None:
                return False

            pending = self.mempool.get_pending_transactions()

            for pending_transaction in pending:

                if not ledger.apply_transaction(pending_transaction):
                    return False

            if not ledger.apply_transaction(transaction_data):
                return False

            return self.mempool.add_transaction(transaction)

        except Exception:
            return False

    def create_block(self, transactions):

        if not isinstance(transactions, list) or not transactions:
            raise ValueError("Block must contain transactions.")

        ledger = self._rebuild_balances()

        if ledger is None:
            raise ValueError("Cannot rebuild blockchain balances.")

        for transaction in transactions:

            if not ledger.apply_transaction(transaction):
                raise ValueError("Block contains an invalid transaction.")

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "transactions": transactions,
            "previous_hash": self.chain[-1]["hash"]
        }

        block["hash"] = self.calculate_hash(block)

        self.chain.append(block)

        return block
            def mine_pending_transactions(self):

        pending = self.mempool.get_pending_transactions()

        if not pending:
            return None

        ledger = self._rebuild_balances()

        if ledger is None:
            return None

        accepted = []

        for transaction in pending:

            if ledger.apply_transaction(transaction):
                accepted.append(transaction)

        if not accepted:
            return None

        block = self.create_block(accepted)

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

                if not required_fields.issubset(block):
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

                    if not isinstance(
                        block.get("genesis_allocations"),
                        dict
                    ):
                        return False

                    if not block["genesis_allocations"]:
                        return False

                else:

                    if block["previous_hash"] != self.chain[i - 1]["hash"]:
                        return False

                    if "genesis_allocations" in block:
                        return False

                for transaction in block["transactions"]:

                    if not self.verify_transaction(transaction):
                        return False

                    transaction_id = transaction["transaction_id"]

                    if transaction_id in seen_transaction_ids:
                        return False

                    seen_transaction_ids.add(transaction_id)

            return self._rebuild_balances() is not None

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

            self.genesis_allocations = dict(
                self.chain[0]["genesis_allocations"]
            )

            print("NOVARA blockchain loaded successfully.")
            return True

        self.chain = original_chain

        print("Invalid blockchain file.")

        return False


if __name__ == "__main__":

    print("==============================")
    print("NOVARA BLOCKCHAIN 0.9.0")
    print("==============================")
    print("Balance-aware validation enabled.")
