"""
NOVARA BLOCKCHAIN
Module: Consensus Engine
Version: 0.1.0

Prototype of a Proof-of-Stake consensus mechanism.
"""

import hashlib
import time


class NovaraConsensus:

    def __init__(self, minimum_stake=100):
        self.minimum_stake = minimum_stake
        self.validators = {}

    def register_validator(self, wallet_address, stake):

        if not wallet_address:
            return False

        if not isinstance(stake, (int, float)):
            return False

        if stake < self.minimum_stake:
            return False

        if wallet_address in self.validators:
            return False

        self.validators[wallet_address] = stake

        return True

    def remove_validator(self, wallet_address):

        if wallet_address not in self.validators:
            return False

        del self.validators[wallet_address]

        return True

    def get_validators(self):
        return self.validators.copy()

    def select_validator(self, block_height):

        if not self.validators:
            return None

        total_stake = sum(self.validators.values())

        seed = hashlib.sha256(
            str(block_height).encode()
        ).hexdigest()

        selection = int(seed, 16) % total_stake

        current = 0

        for address, stake in sorted(self.validators.items()):
            current += stake

            if selection < current:
                return address

        return None


if __name__ == "__main__":

    consensus = NovaraConsensus(minimum_stake=100)

    consensus.register_validator("NOVARA_WALLET_A", 500)
    consensus.register_validator("NOVARA_WALLET_B", 300)

    print("================================")
    print("      NOVARA CONSENSUS")
    print("================================")

    print("Consensus: Proof of Stake")
    print("Validators:", consensus.get_validators())

    selected = consensus.select_validator(block_height=1)

    print("Selected Validator:", selected)
