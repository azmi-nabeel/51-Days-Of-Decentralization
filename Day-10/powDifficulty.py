'''
Day-10: 
Learnt how to stabilise block minting rate by adjusting proof of work difficulty.
Added the difficulty adjustment to the sample blockchain created.
'''

import hashlib
import time
import rsa

# Transaction class remains unchanged
class Transaction:
    def __init__(self, sender_public_key, receiver, amount, signature=None):
        self.sender_public_key = sender_public_key
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def sign_transaction(self, private_key):
        transaction_data = f"{self.sender_public_key}{self.receiver}{self.amount}"
        self.signature = rsa.sign(transaction_data.encode(), private_key, 'SHA-256')

    def verify_transaction(self):
        if self.signature is None:
            return False
        transaction_data = f"{self.sender_public_key}{self.receiver}{self.amount}"
        try:
            rsa.verify(transaction_data.encode(), self.signature, self.sender_public_key)
            return True
        except:
            return False

    def __repr__(self):
        return f"{self.sender_public_key} -> {self.receiver}: {self.amount}"

# Block class with timestamp for difficulty adjustment
class Block:
    def __init__(self, index, transactions, previous_hash, difficulty=2):
        self.index = index
        self.transactions = transactions  # List of transactions
        self.timestamp = time.time()
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
        print(f"Timestamp: {time.ctime(self.timestamp)}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Hash: {self.hash}")
        print(f"Nonce: {self.nonce}")
        print("-" * 30)


# Wallet class remains unchanged
class Wallet:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(512)

    def create_transaction(self, receiver, amount):
        transaction = Transaction(self.public_key, receiver, amount)
        transaction.sign_transaction(self.private_key)
        return transaction


# Blockchain class with difficulty adjustment mechanism
class Blockchain:
    def __init__(self, block_time_target=5):
        self.chain = [self.create_genesis_block()]
        self.transaction_pool = []
        self.block_time_target = block_time_target  # Target time to mine each block (in seconds)

    def create_genesis_block(self):
        return Block(0, [], "0", difficulty=2)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        # Adjust difficulty before mining
        self.adjust_difficulty(new_block)
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block()
        self.chain.append(new_block)

    def adjust_difficulty(self, new_block):
        latest_block = self.get_latest_block()
        time_difference = new_block.timestamp - latest_block.timestamp

        if time_difference < self.block_time_target:
            # Increase difficulty if blocks are mined too quickly
            new_block.difficulty = latest_block.difficulty + 1
        elif time_difference > self.block_time_target:
            # Decrease difficulty if blocks are mined too slowly
            new_block.difficulty = max(1, latest_block.difficulty - 1)
        else:
            # Keep difficulty the same
            new_block.difficulty = latest_block.difficulty

    def add_transaction_to_pool(self, transaction):
        if transaction.verify_transaction():
            self.transaction_pool.append(transaction)
        else:
            print("Transaction is invalid and was not added to the pool.")

    def mine_pending_transactions(self):
        if len(self.transaction_pool) > 0:
            new_block = Block(len(self.chain), self.transaction_pool, self.get_latest_block().hash)
            self.add_block(new_block)

            # Clear the transaction pool after mining
            self.transaction_pool = []
        else:
            print("No transactions to mine!")

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

    # Create wallets for Alice and Bob
    alice_wallet = Wallet()
    bob_wallet = Wallet()

    # Create a transaction from Alice to Bob and add it to the transaction pool
    transaction1 = alice_wallet.create_transaction(bob_wallet.public_key, 50)
    blockchain.add_transaction_to_pool(transaction1)

    # Mine the pending transactions
    blockchain.mine_pending_transactions()

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
Timestamp: Wed Sep 25 18:10:56 2024
Previous Hash: 0
Hash: 75c53d27395ed6af74823796db9555514bb02a84b97140374197d4c46a7c28d1
Nonce: 0
------------------------------
Block #1
Transactions: [PublicKey(6805081917450200284549661667120285193443333942015951442985980362905967250251419270734100275778687747576308495994402075147523325455601812788119850496133571, 65537) -> PublicKey(8543497733679032822089612527139385966865128273335515607858077433161039774775004302478083144594364129471919626347411439435186939696732542332054019389269873, 65537): 50]
Timestamp: Wed Sep 25 18:10:56 2024
Previous Hash: 75c53d27395ed6af74823796db9555514bb02a84b97140374197d4c46a7c28d1
Hash: 0003e928f5b91478de09ff36db0853a721758dae4f1094cff1d3b68e3b7a8fcb
Nonce: 1637
------------------------------
'''
