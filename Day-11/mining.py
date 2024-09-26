'''
Day-11: 
Learnt about how mining works. Understood about how real world cryptos implement mining rewards and transaction fees.
Tried to mirror how rewards and transaction fees work in an abstract way.
'''

import hashlib
import time
import rsa

# Transaction class with fees
class Transaction:
    def __init__(self, sender_public_key, receiver, amount, fee=0, signature=None):
        self.sender_public_key = sender_public_key
        self.receiver = receiver
        self.amount = amount
        self.fee = fee  # Fee for miners
        self.signature = signature

    def sign_transaction(self, private_key):
        transaction_data = f"{self.sender_public_key}{self.receiver}{self.amount}{self.fee}"
        self.signature = rsa.sign(transaction_data.encode(), private_key, 'SHA-256')

    def verify_transaction(self):
        if self.signature is None:
            return False
        transaction_data = f"{self.sender_public_key}{self.receiver}{self.amount}{self.fee}"
        try:
            rsa.verify(transaction_data.encode(), self.signature, self.sender_public_key)
            return True
        except:
            return False

    def __repr__(self):
        return f"{self.sender_public_key} -> {self.receiver}: {self.amount} (Fee: {self.fee})"


# Block class now includes miner reward
class Block:
    def __init__(self, index, transactions, previous_hash, miner_address, reward, difficulty=2):
        self.index = index
        self.transactions = transactions  # List of transactions
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.miner_address = miner_address  # Address of the miner
        self.reward = reward  # Mining reward
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transactions_str = ''.join(str(tx) for tx in self.transactions)
        hash_data = f"{self.index}{self.timestamp}{transactions_str}{self.previous_hash}{self.nonce}{self.miner_address}{self.reward}"
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
        print(f"Miner Address: {self.miner_address}")
        print(f"Reward: {self.reward}")
        print(f"Hash: {self.hash}")
        print(f"Nonce: {self.nonce}")
        print("-" * 30)


# Wallet class remains the same
class Wallet:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(512)

    def create_transaction(self, receiver, amount, fee=0):
        transaction = Transaction(self.public_key, receiver, amount, fee)
        transaction.sign_transaction(self.private_key)
        return transaction


# Blockchain class with mining reward mechanism
class Blockchain:
    def __init__(self, block_time_target=5, mining_reward=50):
        self.chain = [self.create_genesis_block()]
        self.transaction_pool = []
        self.block_time_target = block_time_target  # Target time to mine each block (in seconds)
        self.mining_reward = mining_reward  # Reward for mining a block

    def create_genesis_block(self):
        return Block(0, [], "0", miner_address=None, reward=0, difficulty=2)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        self.adjust_difficulty(new_block)
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block()
        self.chain.append(new_block)

    def adjust_difficulty(self, new_block):
        latest_block = self.get_latest_block()
        time_difference = new_block.timestamp - latest_block.timestamp

        if time_difference < self.block_time_target:
            new_block.difficulty = latest_block.difficulty + 1
        elif time_difference > self.block_time_target:
            new_block.difficulty = max(1, latest_block.difficulty - 1)
        else:
            new_block.difficulty = latest_block.difficulty

    def add_transaction_to_pool(self, transaction):
        if transaction.verify_transaction():
            self.transaction_pool.append(transaction)
        else:
            print("Transaction is invalid and was not added to the pool.")

    def mine_pending_transactions(self, miner_address):
        if len(self.transaction_pool) > 0:
            # Calculate total fees from all transactions
            total_fees = sum(tx.fee for tx in self.transaction_pool)

            # Add a reward transaction for the miner
            reward_transaction = Transaction(None, miner_address, self.mining_reward + total_fees)
            self.transaction_pool.append(reward_transaction)

            # Create a new block with the pending transactions
            new_block = Block(len(self.chain), self.transaction_pool, self.get_latest_block().hash, miner_address, self.mining_reward)

            # Add the block to the chain and clear the transaction pool
            self.add_block(new_block)
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

    # Create a transaction from Alice to Bob with a fee
    transaction1 = alice_wallet.create_transaction(bob_wallet.public_key, 50, fee=2)
    blockchain.add_transaction_to_pool(transaction1)

    # Create another transaction from Bob to Alice with a fee
    transaction2 = bob_wallet.create_transaction(alice_wallet.public_key, 30, fee=1)
    blockchain.add_transaction_to_pool(transaction2)

    # Mine the pending transactions with Alice as the miner
    blockchain.mine_pending_transactions(alice_wallet.public_key)

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
Timestamp: Thu Sep 26 18:18:16 2024
Previous Hash: 0
Miner Address: None
Reward: 0
Hash: 9e320e1ce4a5ff6b1fa55251dd365e96a804eb6a7abb4111d1d6c2a0e3b917a1
Nonce: 0
------------------------------
Block #1
Transactions: [PublicKey(6942752262196527124660030869590574619719932612788893615706172918491495843956143278596166022228494893633351295729629598398370590808844389288307331675801887, 65537) -> PublicKey(7566403563243617296040574449475732369508512337721384494494231902229425118101261028940504457869190954509644977448904335371935265386902408745949967288234821, 65537): 50 (Fee: 2), PublicKey(7566403563243617296040574449475732369508512337721384494494231902229425118101261028940504457869190954509644977448904335371935265386902408745949967288234821, 65537) -> PublicKey(6942752262196527124660030869590574619719932612788893615706172918491495843956143278596166022228494893633351295729629598398370590808844389288307331675801887, 65537): 30 (Fee: 1), None -> PublicKey(6942752262196527124660030869590574619719932612788893615706172918491495843956143278596166022228494893633351295729629598398370590808844389288307331675801887, 65537): 53 (Fee: 0)]
Timestamp: Thu Sep 26 18:18:16 2024
Previous Hash: 9e320e1ce4a5ff6b1fa55251dd365e96a804eb6a7abb4111d1d6c2a0e3b917a1
Miner Address: PublicKey(6942752262196527124660030869590574619719932612788893615706172918491495843956143278596166022228494893633351295729629598398370590808844389288307331675801887, 65537)
Reward: 50
Hash: 000a17d4d5dc82c0921db8f6545d02980cf5e844edb2dbbd27b4afde51c2e488
Nonce: 13
------------------------------
'''