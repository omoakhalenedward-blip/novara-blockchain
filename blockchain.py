"""
NOVARA BLOCKCHAIN
Module: Blockchain Manager
Version: 0.1.0

Responsible for managing the blockchain.
"""

from novara import NovaraBlockchain


class BlockchainManager:

    def __init__(self):
        self.blockchain = NovaraBlockchain()

    def add_block(self, data):
        return self.blockchain.create_block(data)

    def validate(self):
        return self.blockchain.verify_chain()

    def get_chain(self):
        return self.blockchain.chain

    def get_latest_block(self):
        return self.blockchain.chain[-1]


if __name__ == "__main__":

    novara = BlockchainManager()

    print("================================")
    print("       NOVARA BLOCKCHAIN")
    print("================================")

    print("Network: NOVARA")
    print("Version: 0.1.0")
    print("Status:", "VALID" if novara.validate() else "INVALID")
    print("Blocks:", len(novara.get_chain()))
