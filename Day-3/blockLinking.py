'''
Day-3: 
Learnt about structure of a blockchain. How blocks/nodes are linked using previous hash.
Short program to mimick a blockchain.
'''
import hashlib
import time

# Function to calculate SHA-256 hash
def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Block class to represent each block in the blockchain
class Block:
    def __init__(self, index, data, previous_hash):
        #Constructor to initialise each block object(node)
        self.index = index
        self.data = data
        self.timestamp = time.ctime()
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    # Function to calculate the block's hash
    def calculate_hash(self):
        hash_data = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return sha256(hash_data)

    # Function to print the details of the block oject(node)
    def print_block(self):
        print(f"Block #{self.index}")
        print(f"Data: {self.data}")
        print(f"Timestamp: {self.timestamp}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Hash: {self.hash}")
        print("-" * 30)
        # print formatting

# Main to create the blockchain
if __name__ == "__main__":
    # Create the genesis block
    # Since genesis block is the first one there is no previous hash value so 0
    genesis_block = Block(0, "Genesis Block", "0")
    genesis_block.print_block()

    # Create a second block
    second_block = Block(1, "Second Block", genesis_block.hash)
    second_block.print_block()

'''
Output On Running


Block #0
Data: Genesis Block
Timestamp: Wed Sep 18 12:24:20 2024
Previous Hash: 0
Hash: 0b69239370ed2712987a662151cb94a7f8a6746f4937a9dd71cb93e2f24623af
--------------------------------------------------
Block #1
Data: Second Block
Timestamp: Wed Sep 18 12:24:20 2024
Previous Hash: 0b69239370ed2712987a662151cb94a7f8a6746f4937a9dd71cb93e2f24623af
Hash: c8a117724991ee7079fa0ef3f7e03ca47a8e36a02c2e347c5fe1288cddfc09b6
--------------------------------------------------

'''
