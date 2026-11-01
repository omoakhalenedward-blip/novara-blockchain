"""
NOVARA BLOCKCHAIN
Module: Mempool
Version: 1.0.0

Manages, validates and stores pending transactions.
"""

from transactions import Transaction


class NovaraMempool:

    def __init__(self, max_transactions=1000):

        if not isinstance(max_transactions, int):
            raise ValueError("Maximum must be an integer.")

        if max_transactions <= 0:
            raise ValueError("Maximum must be greater than zero.")

        self.pending_transactions = []
        self.max_transactions = max_transactions

    def add_transaction(self, transaction):

        if not isinstance(transaction, Transaction):
            return False

        if not transaction.verify_integrity():
            return False

        transaction_id = transaction.transaction_id

        if self.get_transaction(transaction_id) is not None:
            return False

        if len(self.pending_transactions) >= self.max_transactions:
            return False

        self.pending_transactions.append(transaction)

        return True

    def get_transaction(self, transaction_id):

        for transaction in self.pending_transactions:

            if transaction.transaction_id == transaction_id:
                return transaction

        return None

    def get_pending_transactions(self):

        return [
            transaction.to_dict()
            for transaction in self.pending_transactions
        ]

    def get_transaction_count(self):

        return len(self.pending_transactions)

    def remove_transaction(self, transaction_id):

        transaction = self.get_transaction(transaction_id)

        if transaction is None:
            return False

        self.pending_transactions.remove(transaction)

        return True

    def clear_mempool(self):

        self.pending_transactions.clear()

    def is_full(self):

        return len(self.pending_transactions) >= self.max_transactions


if __name__ == "__main__":

    mempool = NovaraMempool()

    print("================================")
    print("     NOVARA MEMPOOL 1.0.0")
    print("================================")

    print("Maximum Transactions:", mempool.max_transactions)
    print("Pending Transactions:", mempool.get_transaction_count())
    print("Mempool Full:", mempool.is_full())
