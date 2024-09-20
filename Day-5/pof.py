'''
Day-5: 
Learnt about concepts like Proof of Work, Nonce and basic idea of mining where the hash of a block must meet a certain condition (e.g., start with a certain number of leading zeros) to be valid.
Implemented a short program to understand the basic ideas of proof of work and nonce etc.
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
        self.nonce = 0  # Starts at 0
        self.hash = self.calculate_hash()

    # Function to calculate the block's hash
    def calculate_hash(self):
        hash_data = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(hash_data.encode()).hexdigest()

    # Mining function (Proof-of-Work)
    def mine_block(self):
        target = '0' * self.difficulty  # Target hash condition (leading zeros)
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

    def print_block(self):
        print(f"Block #{self.index}")
        print(f"Data: {self.data}")
        print(f"Timestamp: {self.timestamp}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Hash: {self.hash}")
        print(f"Nonce: {self.nonce}")
        print("-" * 30)

if __name__ == "__main__":
    # Create the genesis block
    genesis_block = Block(0, "Genesis Block", "0")
    genesis_block.mine_block()
    genesis_block.print_block()

    # Create a second block
    second_block = Block(1, "Second Block", genesis_block.hash)
    second_block.mine_block()
    second_block.print_block()


'''
Block mined: 00f20c7c3d75752ad3c4c811f0a92d9496ae9f9b7a097aef435dfba280f4f3be
Block #0
Data: Genesis Block
Timestamp: Fri Sep 20 17:59:21 2024
Previous Hash: 0
Hash: 00f20c7c3d75752ad3c4c811f0a92d9496ae9f9b7a097aef435dfba280f4f3be
Nonce: 326
------------------------------
Block mined: 00532b49db8558f0b98cb600922538a2b747229da75aaa2d72813d78cb52c321
Block #1
Data: Second Block
Timestamp: Fri Sep 20 17:59:21 2024
Previous Hash: 00f20c7c3d75752ad3c4c811f0a92d9496ae9f9b7a097aef435dfba280f4f3be
Hash: 00532b49db8558f0b98cb600922538a2b747229da75aaa2d72813d78cb52c321
Nonce: 119
------------------------------
'''
