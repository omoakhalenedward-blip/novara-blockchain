"""
NOVARA BLOCKCHAIN
Module: Network Configuration
Version: 0.1.0

Central configuration for the NOVARA network.
"""


class NovaraConfig:

    NETWORK_NAME = "NOVARA"
    TICKER = "NVR"
    VERSION = "0.1.0"

    MAX_SUPPLY = 21_000_000

    CONSENSUS = "Proof of Stake"

    TARGET_BLOCK_TIME = 5

    MINIMUM_TRANSACTION_FEE = 0.001

    NETWORK_STATUS = "DEVELOPMENT"

    @classmethod
    def display_config(cls):

        print("================================")
        print("       NOVARA CONFIGURATION")
        print("================================")

        print("Network:", cls.NETWORK_NAME)
        print("Ticker:", cls.TICKER)
        print("Version:", cls.VERSION)
        print("Maximum Supply:", cls.MAX_SUPPLY, "NVR")
        print("Consensus:", cls.CONSENSUS)
        print("Target Block Time:", cls.TARGET_BLOCK_TIME, "seconds")
        print("Minimum Transaction Fee:", cls.MINIMUM_TRANSACTION_FEE)
        print("Network Status:", cls.NETWORK_STATUS)


if __name__ == "__main__":
    NovaraConfig.display_config()
