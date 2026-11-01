"""
NOVARA BLOCKCHAIN
Module: Balance Management
Version: 1.0.0

Manages wallet balances and NVR transfers.
"""

from decimal import Decimal, InvalidOperation

from Config import NovaraConfig
from transactions import Transaction


class NovaraBalances:

    DECIMAL_PLACES = 8

    def __init__(self):

        self.balances = {}
        self.total_supply = Decimal("0")
        self.fee_pool = Decimal("0")
        self.processed_transactions = set()
        self.genesis_initialized = False

        self.max_supply = Decimal(
            str(NovaraConfig.MAX_SUPPLY)
        )

        self.transaction_fee = Decimal(
            str(NovaraConfig.MINIMUM_TRANSACTION_FEE)
        )

    def to_units(self, amount):

        try:
            value = Decimal(str(amount))

            if not value.is_finite() or value <= 0:
                return None

            if value.as_tuple().exponent < -self.DECIMAL_PLACES:
                return None

            return value

        except (InvalidOperation, ValueError, TypeError):
            return None

    def initialize_genesis(self, allocations):

        if self.genesis_initialized:
            return False

        if not isinstance(allocations, dict) or not allocations:
            return False

        new_balances = {}
        supply = Decimal("0")

        for address, amount in allocations.items():

            if not isinstance(address, str) or not address.strip():
                return False

            value = self.to_units(amount)

            if value is None:
                return False

            new_balances[address] = value
            supply += value

        if supply > self.max_supply:
            return False

        self.balances = new_balances
        self.total_supply = supply
        self.genesis_initialized = True

        return True

    def get_balance(self, address):

        return self.balances.get(
            address,
            Decimal("0")
        )

    def get_total_supply(self):

        return self.total_supply

    def get_fee_pool(self):

        return self.fee_pool

    def apply_transaction(self, transaction_data):

        if not self.genesis_initialized:
            return False

        if not isinstance(transaction_data, dict):
            return False

        try:

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

            if not transaction.verify_integrity():
                return False

            transaction_id = transaction.transaction_id

            if transaction_id in self.processed_transactions:
                return False

            sender = transaction.sender
            receiver = transaction.receiver

            if sender == receiver:
                return False

            amount = self.to_units(transaction.amount)

            if amount is None:
                return False

            required_amount = amount + self.transaction_fee

            sender_balance = self.get_balance(sender)

            if sender_balance < required_amount:
                return False

            receiver_balance = self.get_balance(receiver)

            # Check all values before updating balances.
            new_sender_balance = sender_balance - required_amount
            new_receiver_balance = receiver_balance + amount
            new_fee_pool = self.fee_pool + self.transaction_fee

            # Apply the transfer.
            self.balances[sender] = new_sender_balance
            self.balances[receiver] = new_receiver_balance
            self.fee_pool = new_fee_pool

            self.processed_transactions.add(transaction_id)

            return True

        except Exception:
            return False

    def get_wallet_count(self):

        return len(self.balances)

    def get_wallets(self):

        return dict(self.balances)


if __name__ == "__main__":

    balances = NovaraBalances()

    print("================================")
    print("   NOVARA BALANCE ENGINE")
    print("   Version: 1.0.0")
    print("================================")

    print("Maximum Supply:", balances.max_supply, "NVR")
    print("Transaction Fee:", balances.transaction_fee, "NVR")
    print("Genesis Initialized:", balances.genesis_initialized)
