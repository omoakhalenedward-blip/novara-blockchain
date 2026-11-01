"""
NOVARA BLOCKCHAIN
Module: Mempool
Version: 0.2.0

Manages and validates pending transactions.
"""

from transactions import Transaction


class NovaraMempool:

    def __init__(self):
        self.pending_transactions = []

    def add_transaction(self, transaction):

        if not isinstance(transaction, Transaction):
            return False

        if not transaction.verify_integrity():
            return False

        transaction_id = transaction.transaction_id

        for existing in self.pending_transactions:
            if existing.transaction_id == transaction_id:
                return False

        self.pending_transactions.append(transaction)

        return True

    def get_pending_transactions(self):

        return [
            transaction.to_dict()
            for transaction in self.pending_transactions
        ]

    def get_transaction_count(self):
        return len(self.pending_transactions)

    def remove_transaction(self, transaction_id):

        for transaction in self.pending_transactions:
            if transaction.transaction_id == transaction_id:
                self.pending_transactions.remove(transaction)
                return True

        return False

    def clear_mempool(self):
        self.pending_transactions.clear()


if __name__ == "__main__":

    mempool = NovaraMempool()

    transaction = Transaction(
        "NOVARA_WALLET_A",
        "NOVARA_WALLET_B",
        10
    )

    result = mempool.add_transaction(transaction)

    print("================================")
    print("       NOVARA MEMPOOL 0.2.0")
    print("================================")

    print("Transaction Accepted:", result)
    print("Pending Transactions:", mempool.get_transaction_count())
    print("Transactions:", mempool.get_pending_transactions())
