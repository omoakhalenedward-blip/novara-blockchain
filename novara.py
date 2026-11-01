"""
NOVARA BLOCKCHAIN
Version: 0.3.0
Project: NOVARA

Persistent blockchain storage.
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

        required_fields = {
            "index",
            "timestamp",
            "data",
            "previous_hash",
            "hash"
        }

        try:
            for i, block in enumerate(self.chain):

                if not isinstance(block, dict):
                    return False

                if not required_fields.issubset(block.keys()):
                    return False

                if block["index"] != i + 1:
                    return False

                if not isinstance(block["timestamp"], (int, float)):
                    return False

                if block["hash"] != self.calculate_hash(block):
                    return False

                if i == 0:
                    if block["previous_hash"] != "0":
                        return False
                else:
                    if block["previous_hash"] != self.chain[i - 1]["hash"]:
                        return False

            return True

        except (TypeError, ValueError, KeyError):
            return False

    def save_chain(self, filename="novara_chain.json"):

        if not self.verify_chain():
            raise ValueError("Cannot save an invalid blockchain.")

        with open(filename, "w") as file:
            json.dump(self.chain, file, indent=4)

        print("NOVARA blockchain saved successfully.")

    def load_chain(self, filename="novara_chain.json"):

        with open(filename, "r") as file:
            loaded_chain = json.load(file)

        if not isinstance(loaded_chain, list):
            return False

        original_chain = self.chain
        self.chain = loaded_chain

        if self.verify_chain():
            print("NOVARA blockchain loaded successfully.")
            return True

        self.chain = original_chain
        print("Invalid blockchain file.")
        return False


if __name__ == "__main__":

    novara = NovaraBlockchain()

    novara.create_block("NOVARA FIRST TEST BLOCK")

    print(json.dumps(novara.chain, indent=4))

    print("\nBlockchain valid:", novara.verify_chain())
