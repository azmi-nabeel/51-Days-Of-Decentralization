'''
Day-7: 
Learnt about concept of transactions in blockchain.
Implemented the blocks such that they can store multiple transactions and hash them instead of string.
'''
import hashlib
import time

# Transaction class to hold transaction details
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"


# Block class to represent each block in the blockchain
class Block:
    def __init__(self, index, transactions, previous_hash, difficulty=2):
        self.index = index
        self.transactions = transactions  # List of transactions
        self.timestamp = time.ctime()
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transactions_str = ''.join(str(tx) for tx in self.transactions)
        hash_data = f"{self.index}{self.timestamp}{transactions_str}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(hash_data.encode()).hexdigest()

    def mine_block(self):
        target = '0' * self.difficulty
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def print_block(self):
        print(f"Block #{self.index}")
        print(f"Transactions: {self.transactions}")
        print(f"Timestamp: {self.timestamp}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Hash: {self.hash}")
        print(f"Nonce: {self.nonce}")
        print("-" * 30)


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, [], "0")

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

            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} has been tampered!")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} is not properly linked to the previous block!")
                return False

        return True


if __name__ == "__main__":
    # Create a new blockchain
    blockchain = Blockchain()

    # Create a list of transactions for Block 1
    transactions1 = [
        Transaction("Alice", "Bob", 50),
        Transaction("Bob", "Charlie", 25)
    ]
    blockchain.add_block(Block(1, transactions1, blockchain.get_latest_block().hash))

    # Create another list of transactions for Block 2
    transactions2 = [
        Transaction("Charlie", "Dave", 100),
        Transaction("Dave", "Eve", 60)
    ]
    blockchain.add_block(Block(2, transactions2, blockchain.get_latest_block().hash))

    # Validate the blockchain
    if blockchain.is_chain_valid():
        print("Blockchain is valid!")
    else:
        print("Blockchain is not valid!")

    # Print the blockchain
    for block in blockchain.chain:
        block.print_block()


'''
Sample Output:

Blockchain is valid!
Block #0
Transactions: []
Timestamp: Sun Sep 22 17:45:28 2024
Previous Hash: 0
Hash: 55c550e4a5b25bd16cfa301f23dc0f11befa5479b8ad6a6af822e48fe4025803
Nonce: 0
------------------------------
Block #1
Transactions: [Alice -> Bob: 50, Bob -> Charlie: 25]
Timestamp: Sun Sep 22 17:45:28 2024
Previous Hash: 55c550e4a5b25bd16cfa301f23dc0f11befa5479b8ad6a6af822e48fe4025803
Hash: 0025139a43ed0131545a6a9ee9c46cfc5513f873df69445b5bf86105b6fe7c2a
Nonce: 41
------------------------------
Block #2
Transactions: [Charlie -> Dave: 100, Dave -> Eve: 60]
Timestamp: Sun Sep 22 17:45:28 2024
Previous Hash: 0025139a43ed0131545a6a9ee9c46cfc5513f873df69445b5bf86105b6fe7c2a
Hash: 004b45aa36904abfc53419b874026178a59f2361cf6d810fc366de49823fed5a
Nonce: 21
------------------------------
'''
