'''
Day-9: 
Learnt about concept of transaction pools and unconfirmed transactions.
Implemented some code to get overview of these topics.
'''
import hashlib
import time
import rsa

# Transaction class with digital signatures
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

# Block class for holding transactions
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


# Wallet class for managing keys and creating transactions
class Wallet:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(512)

    def create_transaction(self, receiver, amount):
        transaction = Transaction(self.public_key, receiver, amount)
        transaction.sign_transaction(self.private_key)
        return transaction


# Blockchain class with transaction pool and block creation
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.transaction_pool = []  # Unconfirmed transactions

    def create_genesis_block(self):
        return Block(0, [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block()
        self.chain.append(new_block)

    def add_transaction_to_pool(self, transaction):
        if transaction.verify_transaction():
            self.transaction_pool.append(transaction)
        else:
            print("Transaction is invalid and was not added to the pool.")

    def mine_pending_transactions(self):
        if len(self.transaction_pool) > 0:
            # Get all pending transactions and add them to a new block
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

    # Create another transaction and add it to the pool
    transaction2 = bob_wallet.create_transaction(alice_wallet.public_key, 30)
    blockchain.add_transaction_to_pool(transaction2)

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
Sample Output
Blockchain is valid!
Block #0
Transactions: []
Timestamp: Tue Sep 24 18:26:12 2024
Previous Hash: 0
Hash: c9ec50f6fd2603cf745afb8629c802c72df916ad0f2ac6345c290d308d346bc0
Nonce: 0
------------------------------
Block #1
Transactions: [PublicKey(7001920855724541099714256547474356641061400118668776709604410751722589881706519050227980956773898541582441005515455392921144689527581013328621072281648541, 65537) -> PublicKey(9016287106473147096392547718390593304760602639514476742102675248531062734155671728038751313423962209668035490319889151764186107682222045721150842752421323, 65537): 50, PublicKey(9016287106473147096392547718390593304760602639514476742102675248531062734155671728038751313423962209668035490319889151764186107682222045721150842752421323, 65537) -> PublicKey(7001920855724541099714256547474356641061400118668776709604410751722589881706519050227980956773898541582441005515455392921144689527581013328621072281648541, 65537): 30]
Timestamp: Tue Sep 24 18:26:12 2024
Previous Hash: c9ec50f6fd2603cf745afb8629c802c72df916ad0f2ac6345c290d308d346bc0
Hash: 005eb9263fe2d2d6bbd750e68b8bf2a823eeee21100f3c40af926f6bce8576fc
Nonce: 76
------------------------------
'''