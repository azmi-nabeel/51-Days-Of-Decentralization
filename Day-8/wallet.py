'''
Day-8: 
Learnt about concept of wallets and their functionality as well as digital signatures. Learnt about public and private keys and how they
can be used to verify transactions.
Implemented some code to understand an abstracted version of wallets and digital signatures.
'''

import hashlib
import time
import rsa # You'll need to install this library with `pip install rsa`

# Transaction class, now with digital signatures
class Transaction:
    def __init__(self, sender_public_key, receiver, amount, signature=None):
        self.sender_public_key = sender_public_key
        self.receiver = receiver
        self.amount = amount
        self.signature = signature  # Signature is None until signed

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

# Block class remains similar, but now holds signed transactions
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

# Wallet class to generate and manage key pairs
class Wallet:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(512)

    def create_transaction(self, receiver, amount):
        transaction = Transaction(self.public_key, receiver, amount)
        transaction.sign_transaction(self.private_key)
        return transaction


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

    # Create wallets for Alice and Bob
    alice_wallet = Wallet()
    bob_wallet = Wallet()

    # Create a transaction from Alice to Bob
    transaction1 = alice_wallet.create_transaction(bob_wallet.public_key, 50)

    # Verify the transaction
    if transaction1.verify_transaction():
        print("Transaction 1 is valid and signed by Alice.")

    # Add the transaction to a block
    blockchain.add_block(Block(1, [transaction1], blockchain.get_latest_block().hash))

    # Create another transaction from Bob to Alice
    transaction2 = bob_wallet.create_transaction(alice_wallet.public_key, 30)

    # Verify the transaction
    if transaction2.verify_transaction():
        print("Transaction 2 is valid and signed by Bob.")

    # Add the second transaction to a block
    blockchain.add_block(Block(2, [transaction2], blockchain.get_latest_block().hash))

    # Validate the blockchain
    if blockchain.is_chain_valid():
        print("Blockchain is valid!")
    else:
        print("Blockchain is not valid!")

    # Print the blockchain
    for block in blockchain.chain:
        block.print_block()


'''
Sample Output

Transaction 1 is valid and signed by Alice.
Transaction 2 is valid and signed by Bob.
Blockchain is valid!
Block #0
Transactions: []
Timestamp: Mon Sep 23 18:18:04 2024
Previous Hash: 0
Hash: a5f7fa0d5008b9f190a43d7c2b81a5babdea3a4a99f049ca019459595f3cdc01
Nonce: 0
------------------------------
Block #1
Transactions: [PublicKey(9732448160019786902123105428459523101293812733719491361710540533510445751817138798710248950636069065929608938561477097428942836324105586450898462990154789, 65537) -> PublicKey(10018589728567766391852654258888988944428053597769161253696224290345112961266806706818519310334285405364780455287151727200267533561853784643388074771910983, 65537): 50]
Timestamp: Mon Sep 23 18:18:04 2024
Previous Hash: a5f7fa0d5008b9f190a43d7c2b81a5babdea3a4a99f049ca019459595f3cdc01
Hash: 002768992c5778fcaea70ea75bfd49e004ae18d2d3288b63615346599413c8ef
Nonce: 371
------------------------------
Block #2
Transactions: [PublicKey(10018589728567766391852654258888988944428053597769161253696224290345112961266806706818519310334285405364780455287151727200267533561853784643388074771910983, 65537) -> PublicKey(9732448160019786902123105428459523101293812733719491361710540533510445751817138798710248950636069065929608938561477097428942836324105586450898462990154789, 65537): 30]
Timestamp: Mon Sep 23 18:18:04 2024
Previous Hash: 002768992c5778fcaea70ea75bfd49e004ae18d2d3288b63615346599413c8ef
Hash: 002a384b9ff12b7c683df72aaed034fc2e754d87cef19bb82bac7cd21948da12
Nonce: 47
------------------------------
'''
