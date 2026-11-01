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

            required
