"""
NOVARA BLOCKCHAIN
Module: Consensus Engine
Version: 0.2.0

Improved Proof-of-Stake prototype.
"""

import hashlib
import math


class NovaraConsensus:

    def __init__(self, minimum_stake=100):

        if (
            isinstance(minimum_stake, bool)
            or not isinstance(minimum_stake, (int, float))
            or not math.isfinite(minimum_stake)
            or minimum_stake <= 0
        ):
            raise ValueError("Invalid minimum stake.")

        self.minimum_stake = minimum_stake
        self.validators = {}

    def register_validator(self, wallet_address, stake):

        if not isinstance(wallet_address, str):
            return False

        if not wallet_address.strip():
            return False

        if (
            isinstance(stake, bool)
            or not isinstance(stake, (int, float))
            or not math.isfinite(stake)
        ):
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

        if (
            isinstance(block_height, bool)
            or not isinstance(block_height, int)
            or block_height < 1
        ):
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

    print("NOVARA CONSENSUS 0.2.0")
    print("Validators:", consensus.get_validators())
    print("Selected Validator:", consensus.select_validator(1))
