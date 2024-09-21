'''
Day-6: 
Learnt about concept of chain validation in blockchain to detect tampering or broken links between blocks, 
ensuring the blockchain's integrity.
Implemented a validating function to understand how chain chain validation works.
'''

import hashlib
import time

class Block:
    def __init__(self, index, data, previous_hash, difficulty=2):
        self.index = index
        self.data = data
        self.timestamp = time.ctime()
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_data = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(hash_data.encode()).hexdigest()

    def mine_block(self):
        target = '0' * self.difficulty
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def print_block(self):
        print(f"Block #{self.index}")
        print(f"Data: {self.data}")
        print(f"Timestamp: {self.timestamp}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Hash: {self.hash}")
        print(f"Nonce: {self.nonce}")
        print("-" * 30)


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} has been tampered!")
                return False

            # Check if the current block points to the correct previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} is not properly linked to the previous block!")
                return False

        return True


if __name__ == "__main__":
    # Create a new blockchain
    blockchain = Blockchain()

    # Add some blocks to the chain
    blockchain.add_block(Block(1, "Block 1 Data", blockchain.get_latest_block().hash))
    blockchain.add_block(Block(2, "Block 2 Data", blockchain.get_latest_block().hash))

    # Validate the chain
    if blockchain.is_chain_valid():
        print("Blockchain is valid!")
    else:
        print("Blockchain is not valid!")

    # Print the blockchain
    for block in blockchain.chain:
        block.print_block()

'''
Output from Sample Run:

Blockchain is valid!
Block #0
Data: Genesis Block
Timestamp: Sat Sep 21 19:04:34 2024
Previous Hash: 0
Hash: 01eeef379a042b7c8dab4945655b17bb1eea9dfa4efc06e0722beca808e6b00b
Nonce: 0
------------------------------
Block #1
Data: Block 1 Data
Timestamp: Sat Sep 21 19:04:34 2024
Previous Hash: 01eeef379a042b7c8dab4945655b17bb1eea9dfa4efc06e0722beca808e6b00b
Hash: 0084ebe7f13796da8ac6b8a8f082b8062d0a2d5499d349e32cb09861cd8bd13f
Nonce: 320
------------------------------
Block #2
Data: Block 2 Data
Timestamp: Sat Sep 21 19:04:34 2024
Previous Hash: 0084ebe7f13796da8ac6b8a8f082b8062d0a2d5499d349e32cb09861cd8bd13f
Hash: 00cfc26b7bc1077cedaa25aece4cba91ee9ba944a6107f805a88e3b8522f841e
Nonce: 97
------------------------------

'''