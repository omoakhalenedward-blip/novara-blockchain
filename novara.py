"""
NOVARA BLOCKCHAIN
Version: 0.2.0
Project: NOVARA

Enhanced blockchain integrity and security.
"""

import hashlib
import json
import time


class NovaraBlockchain:

    def __init__(self):
        self.chain = []
        self.create_block("NOVARA GENESIS BLOCK")

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

    def create_block(self, data):

        previous_hash = (
            self.chain[-1]["hash"]
            if self.chain else "0"
        )

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash
        }

        block["hash"] = self.calculate_hash(block)

        self.chain.append(block)

        return block

    def verify_chain(self):

        if not self.chain:
            return False

        for i, block in enumerate(self.chain):

            required_fields = {
                "index",
                "timestamp",
                "data",
                "previous_hash",
                "hash"
            }

            if not isinstance(block, dict):
                return False

            if not required_fields.issubset(block.keys()):
                return False

            if block["index"] != i + 1:
                return False

            if block["hash"] != self.calculate_hash(block):
                return False

            if i == 0:

                if block["previous_hash"] != "0":
                    return False

            else:

                previous_block = self.chain[i - 1]

                if block["previous_hash"] != previous_block["hash"]:
                    return False

        return True


if __name__ == "__main__":

    novara = NovaraBlockchain()

    novara.create_block("NOVARA FIRST TEST BLOCK")

    print("\n================================")
    print("       NOVARA BLOCKCHAIN")
    print("================================")

    print(json.dumps(novara.chain, indent=4))

    print("\nBlockchain valid:", novara.verify_chain())
