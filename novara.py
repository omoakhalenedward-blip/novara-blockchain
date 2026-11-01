"""
NOVARA BLOCKCHAIN
Version: 0.9.0

Blockchain with Balance and Transaction Validation.
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

        if not isinstance(genesis_allocations, dict) or not genesis_allocations:
            raise ValueError("Valid genesis allocations are required.")

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

    def _rebuild_balances(self):

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
            raise ValueError("Cannot
